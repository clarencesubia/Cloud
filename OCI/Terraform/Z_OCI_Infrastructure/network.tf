locals {
  vcn_cidr_block   = "10.0.0.0/16"
  first_subnet     = cidrsubnet(local.vcn_cidr_block, 8, 0) # 8 bits turns /16 to 24
  null_destination = "0.0.0.0/0"
}


resource "oci_core_vcn" "first_vcn" {
  cidr_block     = local.vcn_cidr_block
  compartment_id = var.compartment_ocid
  display_name   = "first_vcn"
}


resource "oci_core_internet_gateway" "internet-gateway" {
  compartment_id = var.compartment_ocid
  display_name   = "StudentAC-internet-gateway"
  vcn_id         = oci_core_vcn.first_vcn.id
}

resource "oci_core_service_gateway" "test_service_gateway" {
  compartment_id = var.compartment_ocid
  display_name   = "StudentAC-service-gateway"
  vcn_id         = oci_core_vcn.first_vcn.id
  services {
    service_id = data.oci_core_services.test_oci_services.services[0].id
  }
}

resource "oci_core_nat_gateway" "test_nat_gateway" {
  compartment_id = var.compartment_ocid
  display_name   = "StudentAC-nat-gateway"
  vcn_id         = oci_core_vcn.first_vcn.id
}

resource "oci_core_drg" "test_drg" {
  compartment_id = var.compartment_ocid
  display_name   = "StudentAC-drg"
  timeouts {
    create = "30s"
    delete = "1m"
  }
}

resource "oci_core_drg_attachment" "test_drg_attach" {
  drg_id = oci_core_drg.test_drg.id
  vcn_id = oci_core_vcn.first_vcn.id
}

resource "oci_core_subnet" "first_subnet" {
  vcn_id                     = oci_core_vcn.first_vcn.id
  compartment_id             = var.compartment_ocid
  display_name               = "first_subnet"
  cidr_block                 = local.first_subnet
  prohibit_public_ip_on_vnic = true
  security_list_ids          = [oci_core_security_list.webserver-sec-list.id]
  route_table_id             = oci_core_route_table.webserver-rt.id
}
