output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = aws_api_gateway_deployment.api.invoke_url
}

output "api_ecr_repo" {
  description = "ECR repo URL for api-service"
  value       = aws_ecr_repository.api.repository_url
}

output "worker_ecr_repo" {
  description = "ECR repo URL for worker-service"
  value       = aws_ecr_repository.worker.repository_url
}

output "dynamodb_table" {
  description = "DynamoDB jobs table name"
  value       = aws_dynamodb_table.jobs.name
}