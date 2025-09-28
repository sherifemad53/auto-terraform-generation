terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.region
}


module "vpc" {
  source = "./modules/vpc"
  vpc_name = var.vpc_vpc_name
  vpc_cidr = var.vpc_vpc_cidr
}

module "subnets" {
  source = "./modules/subnet"
  vpc_id = var.subnets_vpc_id
  subnets = var.subnets_subnets
}

module "ec2" {
  source = "./modules/ec2"
  ami = var.ec2_ami
  instance_type = var.ec2_instance_type
  key_name = var.ec2_key_name
  instance_name = var.ec2_instance_name
  subnet_id = var.ec2_subnet_id
  sg_id = var.ec2_sg_id
}

module "sg" {
  source = "./modules/sg"
  vpc_id = var.sg_vpc_id
  name = var.sg_name
  ingress_rules = var.sg_ingress_rules
  egress_rules = var.sg_egress_rules
}
