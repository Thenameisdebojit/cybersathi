// infra/terraform/variables.tf
variable "project_name" {
  type    = string
  default = "cybersathi"
}

variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "aws_az" {
  type    = string
  default = "ap-south-1a"
}

variable "vpc_cidr" {
  type    = string
  default = "10.2.0.0/16"
}

variable "subnet_cidr" {
  type    = string
  default = "10.2.1.0/24"
}

variable "aws_account_suffix" {
  type    = string
  default = "dev"
}

variable "create_rds" {
  type    = bool
  default = false
}

variable "rds_engine_version" {
  type    = string
  default = "14.9"
}

variable "rds_instance_class" {
  type    = string
  default = "db.t3.micro"
}

variable "rds_allocated_storage" {
  type    = number
  default = 20
}

variable "rds_db_name" {
  type    = string
  default = "cybersathi"
}

variable "rds_username" {
  type    = string
  default = "admin"
}

variable "rds_password" {
  type    = string
  default = "change_me"
}
