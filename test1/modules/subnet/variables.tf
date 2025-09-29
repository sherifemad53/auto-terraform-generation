variable "vpc_id" {
  type = string
}

variable "subnets" {
  description = "Map of subnets"
  type = map(object({
    cidr   = string
    az     = string
    public = bool
  }))
}
