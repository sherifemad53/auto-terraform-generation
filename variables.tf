# Global
variable "region" {
  description = "AWS region"
  type        = string
}

variable "vpc_name" {
  description = "VPC name"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
}

variable "subnets" {
  description = "Subnets definition"
  type = map(object({
    cidr   = string
    az     = string
    public = bool
  }))
}

# Security Group
variable "sg_name" {
  description = "Security Group name"
  type        = string
}

variable "sg_allowed_ports" {
  description = "Allowed ingress ports"
  type        = list(number)
}

variable "sg_cidr_blocks" {
  description = "CIDR blocks for ingress"
  type        = list(string)
}

# EC2
variable "ec2_ami" {
  description = "AMI ID for EC2"
  type        = string
}

variable "ec2_instance_type" {
  description = "Instance type for EC2"
  type        = string
}

variable "ec2_key_name" {
  description = "EC2 key pair name"
  type        = string
}

variable "ec2_enable_monitoring" {
  description = "Enable monitoring for EC2"
  type        = bool
}

variable "ec2_instance_name" {
  description = "Name tag for EC2 instance"
  type        = string
}

# S3
variable "s3_bucket_name" {
  description = "S3 bucket name"
  type        = string
}

# ALB
variable "alb_name" {
  description = "ALB name"
  type        = string
}
