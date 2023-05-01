resource "oci_core_network_security_group" "tf_network_security_group" {
    #Required
    compartment_id = var.compartment_ocid
    vcn_id = oci_core_vcn.web_apps_vcn.id

    #Optional
    display_name = "LB-NSG"
}

resource "oci_core_network_security_group_security_rule" "tf_network_security_group_security_rule" {
    network_security_group_id = oci_core_network_security_group.tf_network_security_group.id
    direction = "INGRESS"
    protocol = 6
    source = oci_core_vcn.web_apps_vcn.cidr_block
    source_type = "CIDR_BLOCK"
    tcp_options {

        source_port_range {
            max = 80
            min = 80
        }
    }
}