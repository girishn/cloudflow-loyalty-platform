# API Gateway
resource "aws_api_gateway_rest_api" "main" {
  name        = "${var.project_name}-${var.environment}-api"
  description = "LoyaltyFlow API Gateway"
  
  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-api-gateway"
  }
}

# API Gateway Resources
resource "aws_api_gateway_resource" "customers" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "customers"
}

resource "aws_api_gateway_resource" "customer_proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.customers.id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_resource" "points" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "points"
}

resource "aws_api_gateway_resource" "points_proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.points.id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_resource" "rewards" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "rewards"
}

resource "aws_api_gateway_resource" "rewards_proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_resource.rewards.id
  path_part   = "{proxy+}"
}

# API Gateway Methods
resource "aws_api_gateway_method" "customer_proxy" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.customer_proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "points_proxy" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.points_proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "rewards_proxy" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.rewards_proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

# API Gateway Integrations
resource "aws_api_gateway_integration" "customer_proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_method.customer_proxy.resource_id
  http_method = aws_api_gateway_method.customer_proxy.http_method

  integration_http_method = "POST"
  type                   = "AWS_PROXY"
  uri                    = aws_lambda_function.customer_api.invoke_arn
}

resource "aws_api_gateway_integration" "points_proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_method.points_proxy.resource_id
  http_method = aws_api_gateway_method.points_proxy.http_method

  integration_http_method = "POST"
  type                   = "AWS_PROXY"
  uri                    = aws_lambda_function.points_engine.invoke_arn
}

resource "aws_api_gateway_integration" "rewards_proxy" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  resource_id = aws_api_gateway_method.rewards_proxy.resource_id
  http_method = aws_api_gateway_method.rewards_proxy.http_method

  integration_http_method = "POST"
  type                   = "AWS_PROXY"
  uri                    = aws_lambda_function.rewards_api.invoke_arn
}

# API Gateway Stage
resource "aws_api_gateway_stage" "main" {
  deployment_id = aws_api_gateway_deployment.main.id
  rest_api_id   = aws_api_gateway_rest_api.main.id
  stage_name    = var.environment

#   access_log_settings {
#     destination_arn = aws_cloudwatch_log_group.api_gateway.arn
#     format = jsonencode({
#       requestId      = "$context.requestId"
#       ip            = "$context.identity.sourceIp"
#       caller        = "$context.identity.caller"
#       user          = "$context.identity.user"
#       requestTime   = "$context.requestTime"
#       httpMethod    = "$context.httpMethod"
#       resourcePath  = "$context.resourcePath"
#       status        = "$context.status"
#       protocol      = "$context.protocol"
#       responseLength = "$context.responseLength"
#     })
#   }

  xray_tracing_enabled = true

  tags = {
    Name = "${var.project_name}-${var.environment}-api-stage"
  }
}

# API Gateway Deployment
resource "aws_api_gateway_deployment" "main" {
  depends_on = [
    aws_api_gateway_integration.customer_proxy,
    aws_api_gateway_integration.points_proxy,
    aws_api_gateway_integration.rewards_proxy,
  ]

  rest_api_id = aws_api_gateway_rest_api.main.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.customer_proxy.id,
      aws_api_gateway_resource.points_proxy.id,
      aws_api_gateway_resource.rewards_proxy.id,
      aws_api_gateway_method.customer_proxy.id,
      aws_api_gateway_method.points_proxy.id,
      aws_api_gateway_method.rewards_proxy.id,
      aws_api_gateway_integration.customer_proxy.id,
      aws_api_gateway_integration.points_proxy.id,
      aws_api_gateway_integration.rewards_proxy.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_account" "main" {
  cloudwatch_role_arn = aws_iam_role.api_gateway_logs_role.arn
}