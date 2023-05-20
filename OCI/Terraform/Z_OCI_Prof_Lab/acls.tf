locals {
  ingress = [{
    port        = 22
    protocol    = 6
    description = "Port 22 from VCN"
    source      = oci_core_vcn.web_apps_vcn.cidr_block
    },
    {
      port        = 22
      protocol    = 6
      description = "Port 22 from home"
      source      = local.my_home_ip
    },
    {
      port        = 80
      protocol    = 6
      description = "Port 80"
      source      = oci_core_vcn.web_apps_vcn.cidr_block
  }]
  egress = [{
    port        = 443
    protocol    = 6
    description = "Port 443"
    destination = "0.0.0.0/0"
    },
    {
      port        = 80
      protocol    = 6
      description = "Port 80"
      destination = "0.0.0.0/0"
  }]
}


resource "oci_core_security_list" "private" {
  compartment_id = var.compartment_ocid
  display_name   = "WebSecurity"
  vcn_id         = oci_core_vcn.web_apps_vcn.id

  dynamic "ingress_security_rules" {
    for_each = local.ingress
    content {
      protocol    = ingress_security_rules.value.protocol
      source      = ingress_security_rules.value.source
      description = ingress_security_rules.value.description
      tcp_options {
        max = ingress_security_rules.value.port
        min = ingress_security_rules.value.port
      }
    }
  }

  dynamic "egress_security_rules" {
    for_each = local.egress
    content {
      protocol    = egress_security_rules.value.protocol
      destination = egress_security_rules.value.destination
      description = egress_security_rules.value.description
      tcp_options {
        max = egress_security_rules.value.port
        min = egress_security_rules.value.port
      }
    }
  }
}

resource "oci_core_security_list" "app_to_db" {
  compartment_id = var.compartment_ocid
  display_name   = "App to DB"
  vcn_id         = oci_core_vcn.web_apps_vcn.id

  ingress_security_rules {
    tcp_options {
      max = 22 //SSH
      min = 22
    }
    protocol = 6 //TCP
    source   = oci_core_vcn.db_vcn.cidr_block
  }

  egress_security_rules {
    tcp_options {
      max = 22 //HTTP
      min = 22
    }
    protocol    = 6 //TCP
    destination = oci_core_vcn.db_vcn.cidr_block
  }
}

resource "oci_core_security_list" "db_to_apps" {
  compartment_id = var.compartment_ocid
  display_name   = "DB to Apps"
  vcn_id         = oci_core_vcn.db_vcn.id

  ingress_security_rules {
    tcp_options {
      max = 22 //SSH
      min = 22
    }
    protocol = 6 //TCP
    source   = oci_core_vcn.web_apps_vcn.cidr_block
  }

  egress_security_rules {
    tcp_options {
      max = 22 //HTTP
      min = 22
    }
    protocol    = 6 //TCP
    destination = oci_core_vcn.web_apps_vcn.cidr_block
  }
}