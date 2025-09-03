terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  access_key = var.environment == "dev" ? var.access_key : null
  secret_key = var.environment == "dev" ? var.secret_key : null

  default_tags {
    tags = {
      Project     = "CloudFlow"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}