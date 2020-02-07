provider "aws" {
  region = "eu-west-2"
}

terraform {
  # Intentionally empty. Will be filled by Terragrunt
  backend "s3" {}
}
