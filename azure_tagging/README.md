# Azure VM Tagging by VNet

This Terraform configuration allows you to tag all Virtual Machines that are connected to a specific Azure Virtual Network (VNet), referred to as a VPC by some users.

## Prerequisites

- Terraform installed.
- Azure CLI authenticated (`az login`).
- Permissions to read and update resources in the target Resource Group.

## How it works

1. It fetches the ID of the target VNet (default: `sonet`).
2. It retrieves all Network Interfaces (NICs) within the specified Resource Group.
3. It filters these NICs to find only those associated with subnets belonging to the target VNet.
4. It identifies the Virtual Machines attached to those filtered NICs.
5. It retrieves the current tags of those VMs and merges them with the new tags provided in the `tags` variable.
6. It uses the `azapi_update_resource` to apply the merged tags, ensuring existing metadata is preserved.

## Usage

1. Initialize Terraform:
   ```bash
   terraform init
   ```

2. Create a `terraform.tfvars` file or provide variables on the command line:
   ```hcl
   resource_group_name = "your-resource-group"
   vnet_name           = "sonet"
   tags = {
     Environment = "Production"
     ManagedBy   = "Terraform"
   }
   ```

3. Plan and apply:
   ```bash
   terraform plan
   # If the plan looks correct:
   terraform apply
   ```

## Files

- `providers.tf`: Configures the AzureRM and AzAPI providers.
- `variables.tf`: Defines the input variables.
- `main.tf`: Contains the logic to filter VMs by VNet and merge tags.
- `outputs.tf`: Outputs the IDs of the tagged VMs.
