# String Variable
variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
  default     = "main_vpc"
}

# String Variable
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}
