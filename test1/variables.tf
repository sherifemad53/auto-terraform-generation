variable "region" { type = string,defualt= "${region}"} 
variable "vpc_vpc_name" {}
variable "vpc_vpc_cidr" {}
variable "subnets_vpc_id" {}
variable "subnets_subnets" {}
variable "ec2_ami" {}
variable "ec2_instance_type" {}
variable "ec2_key_name" {}
variable "ec2_instance_name" {}
variable "ec2_subnet_id" {}
variable "ec2_sg_id" {}
variable "sg_vpc_id" {}
variable "sg_name" {}
variable "sg_ingress_rules" {}
variable "sg_egress_rules" {}