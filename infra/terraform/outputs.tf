// infra/terraform/outputs.tf
output "vpc_id" {
  value = aws_vpc.cybersathi_vpc.id
}

output "subnet_id" {
  value = aws_subnet.cybersathi_subnet.id
}

output "s3_bucket" {
  value = aws_s3_bucket.cybersathi_bucket.bucket
}

output "rds_endpoint" {
  value       = length(aws_db_instance.cybersathi_db) > 0 ? aws_db_instance.cybersathi_db[0].address : ""
  description = "RDS endpoint if create_rds=true"
}
