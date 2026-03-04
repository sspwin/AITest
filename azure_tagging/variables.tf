variable "resource_group_name" {
  description = "The name of the Resource Group where the VNet and VMs reside."
  type        = string
}

variable "vnet_name" {
  description = "The name of the VNet (VPC) to filter VMs by."
  default     = "sonet"
  type        = string
}

variable "tags" {
  description = "The map of tags to apply to the VMs."
  type        = map(string)
  default     = {
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}
