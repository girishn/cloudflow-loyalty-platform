# S3 Bucket Notification
resource "aws_s3_bucket_notification" "purchase_data_notification" {
  bucket = var.s3_bucket_name

  lambda_function {
    lambda_function_arn = aws_lambda_function.purchase_processor.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "purchase-data/"
    filter_suffix       = ".csv"
  }

  depends_on = [aws_lambda_permission.s3_invoke_purchase_processor]
}

# Lambda permission for S3
resource "aws_lambda_permission" "s3_invoke_purchase_processor" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.purchase_processor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = var.s3_bucket_arn
}
