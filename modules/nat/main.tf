resource "aws_nat_gateway" "this" {
  allocation_id = var.eip_allocation_id
  subnet_id     = var.subnet_id

  tags = {
    Name = var.name
  }
}
