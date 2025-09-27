region   = "us-east-1"
vpc_name = "my-vpc"
vpc_cidr = "10.0.0.0/16"

subnets = {
  public-1 = { cidr = "10.0.1.0/24", az = "us-east-1a", public = true }
  public-2 = { cidr = "10.0.2.0/24", az = "us-east-1b", public = true }
  private-1 = { cidr = "10.0.3.0/24", az = "us-east-1a", public = false }
  private-2 = { cidr = "10.0.4.0/24", az = "us-east-1b", public = false }
}

sg_name          = "main-sg"
sg_allowed_ports = [22, 80, 443]
sg_cidr_blocks   = ["0.0.0.0/0"]

ec2_ami               = "ami-0360c520857e3138f"
ec2_instance_type     = "t2.micro"
ec2_key_name          = "my-keypair"
ec2_enable_monitoring = false
ec2_instance_name     = "my-ec2"

s3_bucket_name = "my-tf-bucket-2025"

alb_name = "my-alb"
