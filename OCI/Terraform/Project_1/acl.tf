resource "oci_core_security_list" "webserver-sec-list" {
  compartment_id = var.compartment_ocid
  display_name = "StudentAC-webserver-sec-list"
  vcn_id = oci_core_vcn.test_vcn.id

  egress_security_rules {
    protocol = 6 //TCP
    destination = "0.0.0.0/0"
  }

  egress_security_rules {
    protocol = 1 //ICMP
    destination = "0.0.0.0/0"
  }

  ingress_security_rules {
    protocol = 6 //TCP
    source = oci_core_vcn.test_vcn.cidr_block
  }

  ingress_security_rules {
    tcp_options {
      max = 22 //SSH
      min = 22
    }
    protocol = 6 //TCP
    source = "0.0.0.0/0"
  }

  ingress_security_rules {
    tcp_options {
      max = 80 //HTTP
      min = 80
    }
    protocol = 6 //TCP
    source = "0.0.0.0/0"
  }

  ingress_security_rules {
    protocol = 1 //ICMP
    source = "0.0.0.0/0"
  }
}
