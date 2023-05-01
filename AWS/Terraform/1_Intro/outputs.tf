output "instance_ip_address" {
  value = aws_instance.app_server.public_ip
}