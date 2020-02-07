data "aws_vpc" "default" {
  default = true
}

data "aws_subnet" "default_public" {
  id = "subnet-d563efaf"
}

data "aws_security_group" "default" {
  name = "default"
  vpc_id = data.aws_vpc.default.id
}

data "aws_ami" "amazon_linux" {
  most_recent = true

  owners = ["amazon"]

  filter {
    name = "name"

    values = [
      "amzn2-ami-hvm-*-x86_64-gp2",
    ]
  }

  filter {
    name = "owner-alias"

    values = [
      "amazon",
    ]
  }
}

data "terraform_remote_state" "s3" {
  backend = "s3"
  config = {
    bucket = "terraform.interview.sensat"
    key = "s3/terraform.tfstate"
    region = "eu-west-2"
  }
}

resource "aws_security_group" "allow_api" {
  name = "allow_api"
  description = "Allow API instance inbound traffic"
  vpc_id = data.aws_vpc.default.id

  ingress {
    from_port = 8000
    to_port = 8000
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_role" "instance_role" {
  name = "instance_role"

  assume_role_policy = jsonencode(
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Principal": {
            "Service": "ec2.amazonaws.com"
          },
          "Effect": "Allow",
          "Sid": ""
        }
      ]
    }
  )
}

resource "aws_iam_role_policy" "instance_policy" {
  name = "instance_policy"
  role = aws_iam_role.instance_role.id

  policy = jsonencode(
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": [
            "ecr:GetAuthorizationToken",
            "ecr:GetDownloadUrlForLayer",
            "ecr:BatchGetImage",
            "ecr:BatchCheckLayerAvailability"
          ],
          "Effect": "Allow",
          "Resource": "*"
        },
        {
          "Action": [
            "s3:GetObject",
            "s3:HeadObject",
          ],
          "Effect": "Allow",
          "Resource": "${data.terraform_remote_state.s3.outputs.config_bucket_arn}/*"

        }
      ]
    }
  )
}

resource "aws_iam_instance_profile" "instance_profile" {
  name = "instance_profile"
  role = aws_iam_role.instance_role.name
}


resource "aws_instance" "sensat" {
  ami = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"

  subnet_id = data.aws_subnet.default_public.id
  vpc_security_group_ids  = [
    data.aws_security_group.default.id,
    aws_security_group.allow_api.id
  ]

  key_name = "default"

  user_data = file("setup-instance.sh")
  iam_instance_profile = aws_iam_instance_profile.instance_profile.name

  tags = {
    Name = "sensat"
  }

  depends_on = [
    aws_security_group.allow_api,
  ]
}
