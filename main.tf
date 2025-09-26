terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.0"

    }
  }
}

provider "aws" {
  region = var.region
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "main_vpc"
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  tags = {
    Name = "public_subnet"
  }
  map_public_ip_on_launch = true
}


resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "main_igw"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "public_rt"
  }
}

resource "aws_route_table_association" "public_rt_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}


module "ec2" {
  source            = "./modules/ec2"
  subnet_id         = aws_subnet.public_subnet.id
  instance_name     = var.ec2.instance_name
  ami               = var.ec2.ami
  instance_type     = var.ec2.instance_type
  key_name          = var.ec2.key_name
  vpc_id            = aws_vpc.main.id
  sg_name           = var.ec2.sg_name
  enable_monitoring = var.ec2.enable_monitoring
  allowed_ports     = var.ec2.allowed_ports
}

