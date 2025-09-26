ec2 = {
  instance_name = "Main_EC2_1"
  ami = "ami-0360c520857e3138f"
  instance_type = "t2.micro"
  key_name = "EC2_Key"
  sg_name = "main_sg"
  enable_monitoring = false
  allowed_ports = [22, 80, 443]
}

