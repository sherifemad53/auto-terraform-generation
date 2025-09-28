variable "name" {
  type        = string
  description = "Name tag for the route table"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID where the route table will be created"
}

variable "routes" {
  description = "List of route objects"
  type = list(object({
    cidr_block                = string
    gateway_id                = optional(string)
    nat_gateway_id            = optional(string)
    transit_gateway_id        = optional(string)
    vpc_peering_connection_id = optional(string)
  }))
  default = []
}

variable "subnet_ids" {
  type        = map(string) # <-- accept map so you know which subnet is which
  description = "Map of subnet IDs to associate with this route table"
}

variable "tags" {
  type        = map(string)
  description = "Additional tags"
  default     = {}
}
