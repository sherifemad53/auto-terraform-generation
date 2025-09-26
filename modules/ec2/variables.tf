variable "ami" {
  description = "The AMI ID for the EC2 instance"
  default     = "ami-0360c520857e3138f"
}
variable "instance_type" {
  description = "The instance type for the EC2 instance"
  default     = "t2.micro"
}
variable "key_name" {
  description = "The key name for the EC2 instance"
  default     = "EC2_Key"
}

variable "enable_monitoring" {
  description = "Enable detailed monitoring for EC2"
  default     = false
}
variable "instance_name" {
  description = "The name of the EC2 instance"
  default     = "EC2_Instance"
}

variable "vpc_id" {
  description = "The VPC ID where the EC2 instance will be deployed"
}

variable "subnet_id" {
  description = "The subnet ID where the EC2 instance will be deployed"
}


variable "sg_name" {
  description = "The name of the security group"
  default     = "main_sg"
}
variable "allowed_ports" {
  type    = list(number)
  default = [22, 80, 443]
}
variable "cidr_blocks" {
  type    = list(string)
  default = ["0.0.0.0/0"]
}

variable "user_data" {
  type    = string
  default = <<-EOF
              #!/bin/bash
              apt update -y
              apt install -y nginx
              systemctl start nginx
              systemctl enable nginx
              EOF
}