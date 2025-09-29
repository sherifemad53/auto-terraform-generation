output "subnet_ids" {
  value = { for k, s in aws_subnet.this : k => s.id }
}


output "public_subnets" {
  value = {
    for k, v in aws_subnet.this : k => v.id if var.subnets[k].public
  }
}

output "private_subnets" {
  value = {
    for k, v in aws_subnet.this : k => v.id if !var.subnets[k].public
  }
}