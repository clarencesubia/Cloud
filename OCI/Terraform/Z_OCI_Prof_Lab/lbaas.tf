resource "oci_load_balancer_load_balancer" "web_load_balancer" {
  #Required
  compartment_id = var.compartment_ocid
  display_name   = "WebLB-Terraform"
  shape          = "flexible"
  subnet_ids     = [oci_core_subnet.web_subnet.id, oci_core_subnet.lb_subnet.id]

  shape_details {
    #Required
    maximum_bandwidth_in_mbps = "1000"
    minimum_bandwidth_in_mbps = "10"
  }
}

resource "oci_load_balancer_backend_set" "my_backend_set" {
  name             = "my-backend-set"
  policy           = "ROUND_ROBIN"
  load_balancer_id = oci_load_balancer_load_balancer.web_load_balancer.id
  health_checker {
    protocol          = "HTTP"
    url_path          = "/"
    retries           = 3
    timeout_in_millis = 3000
    return_code = 200
  }
}

resource "oci_load_balancer_backend" "my_backend1" {
  ip_address       = oci_core_instance.vm_instances[0].private_ip
  port             = 80
  backendset_name  = oci_load_balancer_backend_set.my_backend_set.name
  load_balancer_id = oci_load_balancer_load_balancer.web_load_balancer.id
}

resource "oci_load_balancer_backend" "my_backend2" {
  ip_address       = oci_core_instance.vm_instances[1].private_ip
  port             = 80
  backendset_name  = oci_load_balancer_backend_set.my_backend_set.name
  load_balancer_id = oci_load_balancer_load_balancer.web_load_balancer.id
}

resource "oci_load_balancer_listener" "my_lb_listener" {
  name                     = "my-lb-listener"
  port                     = 80
  protocol                 = "HTTP"
  default_backend_set_name = oci_load_balancer_backend_set.my_backend_set.name
  load_balancer_id         = oci_load_balancer_load_balancer.web_load_balancer.id
}