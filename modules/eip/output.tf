output "eip_id" {
  description = "The ID of the Elastic IP"
  value       = aws_eip.this.id
}

output "eip_allocation_id" {
  description = "The allocation ID of the Elastic IP"
  value       = aws_eip.this.id
}
