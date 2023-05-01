output "my_ads" {
  value = flatten(data.oci_identity_availability_domains.tenancy_availability_domains.availability_domains[*]["name"])
}

output "my_web_subnet" {
  value = oci_core_subnet.web_subnet.cidr_block
}

output "my_lb_public" {
  value = oci_load_balancer_load_balancer.web_load_balancer.ip_addresses
}

output "my_instance_private" {
  value = oci_core_instance.vm_instances[*]["private_ip"]
}

output "my_instance_public" {
  value = oci_core_instance.vm_instances[*]["public_ip"]
}

