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

# VPC
module "vpc" {
  source    = "./modules/vpc"
  vpc_name  = var.vpc_name
  vpc_cidr  = var.vpc_cidr
}

# Subnets
module "subnet" {
  source  = "./modules/subnet"
  vpc_id  = module.vpc.vpc_id
  subnets = var.subnets
}

# Internet Gateway
module "igw" {
  source = "./modules/igw"
  vpc_id = module.vpc.vpc_id
  name   = "${var.vpc_name}-igw"
}

# Elastic IP
module "eip" {
  source = "./modules/eip"
  name   = "${var.vpc_name}-eip"
}

# NAT Gateway
module "nat_gateway" {
  source            = "./modules/nat"
  subnet_id         = values(module.subnet.subnet_ids)[0]
  eip_allocation_id = module.eip.eip_allocation_id
  name              = "${var.vpc_name}-nat"
}

# Security Group
module "sg" {
  source        = "./modules/sg"
  vpc_id        = module.vpc.vpc_id
  name          = var.sg_name
  allowed_ports = var.sg_allowed_ports
  cidr_blocks   = var.sg_cidr_blocks
}

# EC2
module "ec2" {
  source            = "./modules/ec2"
  ami               = var.ec2_ami
  instance_type     = var.ec2_instance_type
  key_name          = var.ec2_key_name
  enable_monitoring = var.ec2_enable_monitoring
  instance_name     = var.ec2_instance_name
  vpc_id            = module.vpc.vpc_id
  subnet_id         = values(module.subnet.subnet_ids)[0]
  sg_id             = module.sg.sg_id
}

# S3
module "s3" {
  source      = "./modules/s3"
  bucket_name = var.s3_bucket_name
}

# ALB
module "alb" {
  source     = "./modules/alb"
  name       = var.alb_name
  sg_id      = module.sg.sg_id
  subnet_ids = values(module.subnet.subnet_ids)
}
