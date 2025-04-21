variable "aws_region" {
  description = "The AWS region to deploy the resources in"
  type        = string
  default     = "us-east-1"
}

variable "aws_access_key" {
  description = "The AWS access key"
  type        = string
  default     = "access-key"
}

variable "aws_secret_key" {
  description = "The AWS secret key"
  type        = string
  default     = "secret-key"
}

variable "aws_bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
  default     = "bucket-name"
}

variable "aws_lambda_function_name" {
  description = "The name of the Lambda function"
  type        = string
  default     = "function-name"
}
