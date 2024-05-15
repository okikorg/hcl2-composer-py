resource "ec2-instance" "vm1" {
  cores  = 2
  memory = 4
}

variable "instance_count" {
  description = "Number of instances to create"
  type        = "number"
  default     = [1]
}
