variable "name" {
  type    = string
  default = "dynamic-sg"
}

variable "vpc_id" {
  type = string
}

variable "allowed_ports" {
  type    = list(number)
  default = [22, 80, 443]
}

variable "cidr_blocks" {
  type    = list(string)
  default = ["0.0.0.0/0"]
}
