output "config_bucket_arn" {
    value = aws_s3_bucket.app_config.arn
    description = "App config bucket ARN"
}
