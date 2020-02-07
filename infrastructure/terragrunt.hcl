remote_state {
  backend = "s3"
  config = {
    bucket = "terraform.interview.sensat"

    key = "${path_relative_to_include()}/terraform.tfstate"
    region = "eu-west-2"
    encrypt = true
    dynamodb_table = "terraform"
  }
}

terraform_version_constraint = "0.12.19"

prevent_destroy = true
