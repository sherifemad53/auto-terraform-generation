variable "name" {
  type = string
  default = "my-alb"
}

variable "sg_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}
