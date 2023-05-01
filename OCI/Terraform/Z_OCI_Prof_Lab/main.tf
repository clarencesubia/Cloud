provider "oci" {
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
  region           = var.region
}


locals {
  vcn_cidr_block   = "10.0.0.0/16"
  first_subnet     = cidrsubnet(local.vcn_cidr_block, 8, 1) # 8 bits turns /16 to 24
  second_subnet    = cidrsubnet(local.vcn_cidr_block, 8, 2)
  third_subnet     = cidrsubnet(local.vcn_cidr_block, 8, 3)
  null_destination = "0.0.0.0/0"
  my_home_ip       = "112.210.231.217/32"
  my_ads           = data.oci_identity_availability_domains.tenancy_availability_domains.availability_domains
}

data "oci_identity_availability_domains" "tenancy_availability_domains" {
  compartment_id = var.tenancy_ocid
}