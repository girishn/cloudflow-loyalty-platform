# DynamoDB Tables
resource "aws_dynamodb_table" "customers" {
  name           = "${var.environment}-customers"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "customerId"

  attribute {
    name = "customerId"
    type = "S"
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-customers"
    Environment = var.environment
  }
}

resource "aws_dynamodb_table" "points" {
  name           = "${var.environment}-points"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "transactionId"

  attribute {
    name = "transactionId"
    type = "S"
  }

  attribute {
    name = "customerId"
    type = "S"
  }

  global_secondary_index {
    name               = "CustomerIndex"
    hash_key           = "customerId"
    projection_type    = "ALL"
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-points"
    Environment = var.environment
  }
}

resource "aws_dynamodb_table" "rewards" {
  name           = "${var.environment}-rewards"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "rewardId"

  attribute {
    name = "rewardId"
    type = "S"
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-rewards"
    Environment = var.environment
  }
}