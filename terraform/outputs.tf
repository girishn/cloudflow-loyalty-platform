output "api_gateway_invoke_url" {
  description = "Invoke URL of the API Gateway"
  value       = module.compute[0].api_gateway_invoke_url
}
