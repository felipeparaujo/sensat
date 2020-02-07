resource "aws_ecr_repository" "sensat" {
  name = "sensat"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
