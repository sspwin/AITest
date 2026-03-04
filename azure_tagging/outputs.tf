output "tagged_vm_ids" {
  description = "List of Virtual Machine IDs that were tagged."
  value       = [for v in local.vms_to_tag : v.id]
}
