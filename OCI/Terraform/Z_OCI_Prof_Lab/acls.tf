resource "oci_core_security_list" "private" {
  compartment_id = var.compartment_ocid
  display_name   = "WebSecurity"
  vcn_id         = oci_core_vcn.web_apps_vcn.id

  ingress_security_rules {
    tcp_options {
      max = 22 //SSH
      min = 22
    }
    protocol = 6 //TCP
    source   = oci_core_vcn.web_apps_vcn.cidr_block
  }

  ingress_security_rules {
    tcp_options {
      max = 80 //HTTP
      min = 80
    }
    protocol = 6 //TCP
    source   = local.my_home_ip
  }

  ingress_security_rules {
    tcp_options {
      max = 22 //HTTP
      min = 22
    }
    protocol = 6 //TCP
    source   = local.my_home_ip
  }

  egress_security_rules {
    tcp_options {
      max = 80 //HTTP
      min = 80
    }
    protocol    = 6 //TCP
    destination = "0.0.0.0/0"
  }
  
  egress_security_rules {
    tcp_options {
      max = 443 //HTTP
      min = 443
    }
    protocol    = 6 //TCP
    destination = "0.0.0.0/0"
  }
}