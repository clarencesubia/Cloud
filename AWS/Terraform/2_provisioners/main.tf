terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.64.0"
    }
  }
  cloud {
    organization = "subiaclarence96"

    workspaces {
      name = "provisioners"
    }
  }
}


provider "aws" {
  region  = "us-east-1"
}


resource "aws_instance" "app_server" {
  ami                    = "ami-02396cdd13e9a1257"
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.allow_http.id]
  user_data              = data.template_file.user_data.rendered
  # provisioner "remote-exec" {
  #   inline = [
  #   "echo ${self.private_ip} >> ~/private_ips.txt"
  #   ]
  #   connection {
  #       type = "ssh"
  #       user = "ec2-user"
  #       host = "${self.public_ip}"
  #   }
  # }
  # provisioner "file" {
  #   content     = "ami used: ${self.ami}"
  #   destination = "/tmp/file.log"
  # }
  
  tags = {
    Name = "Instance-Provisioner"
  }
}

resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = "ssh-rsa xxx"
}


data "aws_vpc" "main" {
  id = "vpc-05f960b03900f9a4c"
}

data "template_file" "user_data" {
  template = file("./cloud-init.yml")
}


resource "aws_security_group" "allow_http" {
  name        = "allow_http_inbound"
  description = "Allow HTTP inbound traffic"
  vpc_id      = data.aws_vpc.main.id

  ingress {
      description      = "HTTP Inbound"
      from_port        = 80
      to_port          = 80
      protocol         = "tcp"
      cidr_blocks      = ["0.0.0.0/0"]
      ipv6_cidr_blocks = []
    }

  egress {
      from_port        = 0
      to_port          = 0
      protocol         = "-1"
      cidr_blocks      = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
    }
}

resource "aws_security_group_rule" "example" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  ipv6_cidr_blocks  = []
  security_group_id = aws_security_group.allow_http.id
}

output "public_ip" {
  value = aws_instance.app_server.public_ip
}

output "http_sg" {
  value = aws_security_group.allow_http.name
}

output "http_sg_id" {
  value = aws_security_group.allow_http.id
}
