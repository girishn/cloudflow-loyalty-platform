variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "access_key" {
  type      = string
  sensitive = true
}

variable "secret_key" {
  type      = string
  sensitive = true
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "cloudflow"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

# Feature flags for staged deployment
variable "enable_compute" {
  description = "Enable compute resources (Stage 1+)"
  type        = bool
  default     = true
}

variable "enable_storage" {
  description = "Enable storage resources (Stage 1+)"
  type        = bool
  default     = true
}

variable "enable_streaming" {
  description = "Enable streaming resources (Stage 2+)"
  type        = bool
  default     = false
}

variable "enable_ml" {
  description = "Enable ML resources (Stage 2+)"
  type        = bool
  default     = false
}

variable "enable_monitoring" {
  description = "Enable advanced monitoring (Stage 3+)"
  type        = bool
  default     = false
}

variable "enable_workflows" {
  description = "Enable workflow orchestration (Stage 3+)"
  type        = bool
  default     = false
}