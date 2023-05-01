locals {
  vcn_cidr_block    = "10.0.0.0/16"
  first_subnet      = cidrsubnet(local.vcn_cidr_block, 8, 0)
}


resource "oci_core_vcn" "first_vcn" {
  cidr_block     = local.vcn_cidr_block
  compartment_id = var.compartment_ocid
  display_name   = "first_vcn"
}


resource "oci_core_subnet" "first_vcn" {
    vcn_id                      = oci_core_vcn.first_vcn.id
    compartment_id              = var.compartment_ocid
    display_name                = "first_subnet"
    cidr_block                  = local.first_subnet
    prohibit_public_ip_on_vnic  = true
}