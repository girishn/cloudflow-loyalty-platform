output "api_gateway_id" {
  value       = aws_api_gateway_rest_api.main.id
}

output "api_gateway_execution_arn" {
  value       = aws_api_gateway_rest_api.main.execution_arn
}

output "api_gateway_invoke_url" {
  description = "Invoke URL of the API Gateway"
  value       = "https://${aws_api_gateway_rest_api.main.id}.execute-api.${var.aws_region}.amazonaws.com/${var.environment}"
}

output "customer_api_function_arn" {
  value       = aws_lambda_function.customer_api.arn
}

output "customer_api_function_name" {
  value       = aws_lambda_function.customer_api.function_name
}

output "points_engine_function_arn" {
  value       = aws_lambda_function.points_engine.arn
}

output "points_engine_function_name" {
  value       = aws_lambda_function.points_engine.function_name
}

output "rewards_api_function_arn" {
  value       = aws_lambda_function.rewards_api.arn
}

output "rewards_api_function_name" {
  value       = aws_lambda_function.rewards_api.function_name
}

output "lambda_execution_role_arn" {
  value       = aws_iam_role.lambda_execution.arn
}

# DynamoDB Table outputs
output "customers_table_name" {
  description = "Name of the customers DynamoDB table"
  value       = aws_dynamodb_table.customers.name
}

output "customers_table_arn" {
  description = "ARN of the customers DynamoDB table"
  value       = aws_dynamodb_table.customers.arn
}

output "points_table_name" {
  description = "Name of the points DynamoDB table"
  value       = aws_dynamodb_table.points.name
}

output "points_table_arn" {
  description = "ARN of the points DynamoDB table"
  value       = aws_dynamodb_table.points.arn
}

output "rewards_table_name" {
  description = "Name of the rewards DynamoDB table"
  value       = aws_dynamodb_table.rewards.name
}

output "rewards_table_arn" {
  description = "ARN of the rewards DynamoDB table"
  value       = aws_dynamodb_table.rewards.arn
}