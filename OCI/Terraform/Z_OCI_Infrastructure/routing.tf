resource "oci_core_route_table" "webserver-rt" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.first_vcn.id
  display_name   = "StudentAC-webserver-rt"
  route_rules {
    destination       = local.null_destination
    network_entity_id = oci_core_internet_gateway.internet-gateway.id
  }
}

resource "oci_core_route_table" "test_nat_rt" {
  compartment_id = var.compartment_ocid
  display_name   = "StudentAC-nat-rt"
  vcn_id         = oci_core_vcn.first_vcn.id

  route_rules {
    destination       = "0.0.0.0/0"
    network_entity_id = oci_core_nat_gateway.test_nat_gateway.id
  }
}