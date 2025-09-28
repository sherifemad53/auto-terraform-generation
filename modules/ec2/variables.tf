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

variable "subnet_id" {
  description = "The subnet ID where the EC2 instance will be deployed"
}


variable "sg_name" {
  description = "The name of the security group"
  default     = "main_sg"
}

variable "sg_id" {
  description = "Security group ID to attach to EC2 instance"
  type        = string
}


variable "user_data" {
  type    = string
  default = ""
}