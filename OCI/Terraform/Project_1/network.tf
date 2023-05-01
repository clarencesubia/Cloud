data "oci_identity_availability_domain" "AD" {
  compartment_id = var.tenancy_ocid
  ad_number = 1
}

resource "oci_core_vcn" "test_vcn" {
  cidr_block     = "192.168.0.0/16"
  compartment_id = var.compartment_ocid
  display_name   = "StudentAC-VCN"
}

resource "oci_core_subnet" "test_subnet" {
  cidr_block     = "192.168.0.0/24"
  compartment_id = var.compartment_ocid
  display_name   = "StudentAC-subnet"
  vcn_id         = oci_core_vcn.test_vcn.id
}

resource "oci_core_internet_gateway" "internet-gateway" {
  compartment_id = var.compartment_ocid
  display_name = "StudentAC-internet-gateway"
  vcn_id = oci_core_vcn.test_vcn.id
}

resource "oci_core_route_table" "webserver-rt" {
  compartment_id = var.compartment_ocid
  vcn_id = oci_core_vcn.test_vcn.id
  display_name = "StudentAC-webserver-rt"
  route_rules {
    destination = "0.0.0.0/0"
    network_entity_id = oci_core_internet_gateway.internet-gateway.id
  }
}