# Data source to get the Virtual Network (VPC)
data "azurerm_virtual_network" "sonet" {
  name                = var.vnet_name
  resource_group_name = var.resource_group_name
}

# Get all Network Interfaces in the Resource Group
data "azurerm_resources" "nics" {
  resource_group_name = var.resource_group_name
  type                = "Microsoft.Network/networkInterfaces"
}

# Fetch detailed info for each NIC to get its Subnet ID and associated VM ID
data "azurerm_network_interface" "nic_info" {
  for_each            = { for r in data.azurerm_resources.nics.resources : r.name => r.name }
  name                = each.key
  resource_group_name = var.resource_group_name
}

# Get all VMs in the resource group to retrieve their current tags for merging
data "azurerm_resources" "vms" {
  resource_group_name = var.resource_group_name
  type                = "Microsoft.Compute/virtualMachines"
}

locals {
  # Filter NICs that belong to the targeted VNet
  # A subnet ID looks like: /subscriptions/.../virtualNetworks/VNET_NAME/subnets/SUBNET_NAME
  vnet_id = data.azurerm_virtual_network.sonet.id

  sonet_nics = [
    for n in data.azurerm_network_interface.nic_info : n
    if n.ip_configuration[0].subnet_id != null && startswith(n.ip_configuration[0].subnet_id, local.vnet_id)
  ]

  # Identify unique VM IDs from these NICs
  vm_ids_in_sonet = distinct([
    for n in local.sonet_nics : n.virtual_machine_id
    if n.virtual_machine_id != null && n.virtual_machine_id != ""
  ])

  # Map of VM ID to current tags for merging
  vm_current_tags = {
    for r in data.azurerm_resources.vms.resources : r.id => r.tags
  }

  # Create a map of VM name (for for_each) to its ID and merged tags
  vms_to_tag = {
    for vm_id in local.vm_ids_in_sonet :
    split("/", vm_id)[length(split("/", vm_id)) - 1] => {
      id   = vm_id
      tags = merge(lookup(local.vm_current_tags, vm_id, {}), var.tags)
    }
  }
}

# Apply merged tags only to VMs in the targeted VNet
resource "azapi_update_resource" "tag_vms" {
  for_each = local.vms_to_tag

  type        = "Microsoft.Compute/virtualMachines@2023-09-01"
  resource_id = each.value.id

  body = jsonencode({
    tags = each.value.tags
  })
}
