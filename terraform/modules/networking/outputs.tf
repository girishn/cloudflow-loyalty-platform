output "vpc_id" {
  value       = aws_vpc.main.id
}

output "vpc_cidr_block" {
  value       = aws_vpc.main.cidr_block
}

output "public_subnets" {
  value       = aws_subnet.public[*].id
}

output "private_app_subnets" {
  value       = aws_subnet.private_app[*].id
}

output "private_data_subnets" {
  value       = aws_subnet.private_data[*].id
}

output "internet_gateway_id" {
  value       = aws_internet_gateway.main.id
}

output "nat_gateway_ids" {
  value       = aws_nat_gateway.main[*].id
}

output "api_gateway_security_group_id" {
  value       = aws_security_group.api_gateway.id
}

output "lambda_security_group_id" {
  value       = aws_security_group.lambda.id
}

output "database_security_group_id" {
  value       = aws_security_group.database.id
}

output "cache_security_group_id" {
  value       = aws_security_group.cache.id
}

output "vpc_endpoints_security_group_id" {
  value       = aws_security_group.vpc_endpoints.id
}