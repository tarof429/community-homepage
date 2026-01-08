output "my-ip" {
  value = var.my_ip
}

output "ami_id" {
  value = data.aws_ami.amazon-linux-image.id
}

output "server-ip" {
  value = aws_instance.webserver.public_ip
}