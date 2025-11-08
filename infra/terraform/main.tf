// infra/terraform/main.tf
terraform {
  required_version = ">= 1.3.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Basic VPC + Subnet (minimal example)
resource "aws_vpc" "cybersathi_vpc" {
  cidr_block = var.vpc_cidr
  tags = { Name = "${var.project_name}-vpc" }
}

resource "aws_subnet" "cybersathi_subnet" {
  vpc_id            = aws_vpc.cybersathi_vpc.id
  cidr_block        = var.subnet_cidr
  availability_zone = var.aws_az
  tags = { Name = "${var.project_name}-subnet" }
}

# Security group for EKS / application (placeholder)
resource "aws_security_group" "cybersathi_sg" {
  name        = "${var.project_name}-sg"
  description = "Security group for CyberSathi services"
  vpc_id      = aws_vpc.cybersathi_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "${var.project_name}-sg" }
}

# RDS (Postgres) minimal - optional, controlled by var.create_rds
resource "aws_db_instance" "cybersathi_db" {
  count                    = var.create_rds ? 1 : 0
  identifier               = "${var.project_name}-db"
  engine                   = "postgres"
  engine_version           = var.rds_engine_version
  instance_class           = var.rds_instance_class
  allocated_storage        = var.rds_allocated_storage
  name                     = var.rds_db_name
  username                 = var.rds_username
  password                 = var.rds_password
  skip_final_snapshot      = true
  publicly_accessible      = false
  vpc_security_group_ids   = [aws_security_group.cybersathi_sg.id]
  db_subnet_group_name     = aws_db_subnet_group.cybersathi_subnets.name
  tags = { Name = "${var.project_name}-rds" }
}

resource "aws_db_subnet_group" "cybersathi_subnets" {
  count = var.create_rds ? 1 : 0
  name  = "${var.project_name}-db-subnets"
  subnet_ids = [aws_subnet.cybersathi_subnet.id]
  tags = { Name = "${var.project_name}-db-subnets" }
}

# S3: storage for backups / artifacts
resource "aws_s3_bucket" "cybersathi_bucket" {
  bucket = "${var.project_name}-artifacts-${var.aws_account_suffix}"
  acl    = "private"

  tags = {
    Name = "${var.project_name}-artifacts"
  }
}
