# Video Event S3 Buckets
resource "aws_s3_bucket" "video_event_bucket" {
  bucket = "${var.aws_bucket_name}-pipeline"
}

# Video Aggregated Event S3 Buckets
resource "aws_s3_bucket" "video_aggregatred_event_bucket" {
  bucket = "${var.aws_bucket_name}-aggregated"
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_execution_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "lambda_s3_policy" {
  name = "lambda_s3_policy"
  role = aws_iam_role.lambda_exec_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::${var.aws_bucket_name}-pipeline/*",
          "arn:aws:s3:::${var.aws_bucket_name}-aggregated/*"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_lambda_function" "process_video_events" {
  function_name    = "process_video_events"
  filename         = "../function.zip"
  source_code_hash = filebase64sha256("../function.zip")
  handler          = "lambda_func.lambda_handler"
  runtime          = "python3.8"
  role             = aws_iam_role.lambda_exec_role.arn
  timeout          = 60
  depends_on       = [aws_iam_role_policy.lambda_s3_policy]
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.process_video_events.function_name
  principal     = "s3.amazonaws.com"

  # Replace with your bucket ARN
  source_arn = aws_s3_bucket.video_event_bucket.arn
}

resource "aws_s3_bucket_notification" "lambda_trigger" {
  bucket = aws_s3_bucket.video_event_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.process_video_events.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "data/input/"
    filter_suffix       = ".txt"
  }

  depends_on = [aws_lambda_permission.allow_s3]
}
