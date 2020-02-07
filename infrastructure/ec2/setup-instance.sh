#!/usr/bin/env bash
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

su ec2-user

$(aws ecr get-login --no-include-email --region eu-west-2)
aws s3 cp s3://config.interview.sensat/config.yml $HOME/config.yml

docker run \
    --mount type=bind,source=$HOME/config.yml,target=/opt/sensat/config.yml \
    -p 8000:8000 \
    322693351111.dkr.ecr.eu-west-2.amazonaws.com/sensat:latest
