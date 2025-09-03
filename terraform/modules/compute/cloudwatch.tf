# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "api_gateway" {
  name              = "/aws/apigateway/${aws_api_gateway_rest_api.main.name}"
  retention_in_days = 14

  tags = {
    Name = "${var.project_name}-${var.environment}-api-gateway-logs"
  }
}

resource "aws_cloudwatch_log_group" "customer_api" {
  name              = "/aws/lambda/${aws_lambda_function.customer_api.function_name}"
  retention_in_days = 14

  tags = {
    Name = "${var.project_name}-${var.environment}-customer-api-logs"
  }
}

resource "aws_cloudwatch_log_group" "points_engine" {
  name              = "/aws/lambda/${aws_lambda_function.points_engine.function_name}"
  retention_in_days = 14

  tags = {
    Name = "${var.project_name}-${var.environment}-points-engine-logs"
  }
}

resource "aws_cloudwatch_log_group" "rewards_api" {
  name              = "/aws/lambda/${aws_lambda_function.rewards_api.function_name}"
  retention_in_days = 14

  tags = {
    Name = "${var.project_name}-${var.environment}-rewards-api-logs"
  }
}