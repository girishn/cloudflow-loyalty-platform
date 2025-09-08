# Lambda Archive Files
data "archive_file" "customer_api" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src/lambda/customer-api"
  output_path = "${path.module}/../../../lambda_packages/customer-api.zip"
}

data "archive_file" "points_engine" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src/lambda/points-engine"
  output_path = "${path.module}/../../../lambda_packages/points-engine.zip"
}

data "archive_file" "rewards_api" {
  type        = "zip"
  source_dir  = "${path.module}/../../../src/lambda/rewards-api"
  output_path = "${path.module}/../../../lambda_packages/rewards-api.zip"
}

# Customer API Lambda Function
resource "aws_lambda_function" "customer_api" {
  filename         = data.archive_file.customer_api.output_path
  function_name    = "${var.project_name}-${var.environment}-customer-api"
  role            = aws_iam_role.lambda_execution.arn
  handler         = "lambda_function.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30
  source_code_hash = data.archive_file.customer_api.output_base64sha256

  # vpc_config {
  #   subnet_ids         = var.private_subnets
  #   security_group_ids = [var.lambda_security_group_id]
  # }

  environment {
    variables = {
      CUSTOMERS_TABLE = aws_dynamodb_table.customers.name
      ENVIRONMENT     = var.environment
      LOG_LEVEL      = "INFO"
    }
  }

  tracing_config {
    mode = "Active"
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-customer-api"
  }
}

# Points Engine Lambda Function
resource "aws_lambda_function" "points_engine" {
  filename         = data.archive_file.points_engine.output_path
  function_name    = "${var.project_name}-${var.environment}-points-engine"
  role            = aws_iam_role.lambda_execution.arn
  handler         = "lambda_function.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30
  source_code_hash = data.archive_file.points_engine.output_base64sha256

  # vpc_config {
  #   subnet_ids         = var.private_subnets
  #   security_group_ids = [var.lambda_security_group_id]
  # }

  environment {
    variables = {
      CUSTOMERS_TABLE = aws_dynamodb_table.customers.name
      POINTS_TABLE    = aws_dynamodb_table.points.name
      ENVIRONMENT     = var.environment
      LOG_LEVEL       = "INFO"
    }
  }

  tracing_config {
    mode = "Active"
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-points-engine"
  }
}

# Rewards API Lambda Function
resource "aws_lambda_function" "rewards_api" {
  filename         = data.archive_file.rewards_api.output_path
  function_name    = "${var.project_name}-${var.environment}-rewards-api"
  role            = aws_iam_role.lambda_execution.arn
  handler         = "lambda_function.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30
  source_code_hash = data.archive_file.rewards_api.output_base64sha256

  # vpc_config {
  #   subnet_ids         = var.private_subnets
  #   security_group_ids = [var.lambda_security_group_id]
  # }

  environment {
    variables = {
      REWARDS_TABLE   = aws_dynamodb_table.rewards.name
      POINTS_TABLE    = aws_dynamodb_table.points.name
      CUSTOMERS_TABLE = aws_dynamodb_table.customers.name
      ENVIRONMENT     = var.environment
      LOG_LEVEL       = "INFO"
    }
  }

  tracing_config {
    mode = "Active"
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-rewards-api"
  }
}

# Lambda Permissions for API Gateway
resource "aws_lambda_permission" "customer_api" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.customer_api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.main.execution_arn}/*/*"
}

resource "aws_lambda_permission" "points_engine" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.points_engine.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.main.execution_arn}/*/*"
}

resource "aws_lambda_permission" "rewards_api" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.rewards_api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.main.execution_arn}/*/*"
}