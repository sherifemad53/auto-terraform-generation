resource "aws_security_group" "main_sg" {
  name        = var.sg_name
  description = "Managed by EC2 module"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.allowed_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = var.cidr_blocks
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "this" {
  ami                    = var.ami
  instance_type          = var.instance_type
  key_name               = var.key_name
  monitoring             = var.enable_monitoring
  vpc_security_group_ids = [aws_security_group.main_sg.id]
  subnet_id              = var.subnet_id

  tags = {
    Name = var.instance_name  
  }

  user_data = var.user_data
}
