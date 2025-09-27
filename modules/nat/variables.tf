variable "subnet_id" {
  type        = string
}

variable "eip_allocation_id" {
  type        = string
}

variable "name" {
  type        = string
  default     = "my-nat-gw"
}
