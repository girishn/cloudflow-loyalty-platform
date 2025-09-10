# S3 Bucket for storing customer data, reports, and ML artifacts
resource "aws_s3_bucket" "loyalty_data" {
  bucket = "${var.project_name}-loyalty-data-${var.environment}-${random_id.bucket_suffix.hex}"
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket_versioning" "loyalty_data" {
  bucket = aws_s3_bucket.loyalty_data.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "loyalty_data" {
  bucket = aws_s3_bucket.loyalty_data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}