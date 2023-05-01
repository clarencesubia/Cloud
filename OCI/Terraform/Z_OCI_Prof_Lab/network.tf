resource "oci_core_vcn" "web_apps_vcn" {
  cidr_block     = local.vcn_cidr_block
  compartment_id = var.compartment_ocid
  display_name   = "WebAppsVCN"
}

resource "oci_core_subnet" "web_subnet" {
  vcn_id              = oci_core_vcn.web_apps_vcn.id
  compartment_id      = var.compartment_ocid
  display_name        = "WebSubnet"
  cidr_block          = local.first_subnet
  availability_domain = local.my_ads[0]["name"]
  security_list_ids          = [oci_core_security_list.private.id]
  route_table_id      = oci_core_route_table.web_app_route.id
}

resource "oci_core_subnet" "apps_subnet" {
  vcn_id                     = oci_core_vcn.web_apps_vcn.id
  compartment_id             = var.compartment_ocid
  display_name               = "AppsSubnet"
  cidr_block                 = local.second_subnet
  prohibit_public_ip_on_vnic = true
  availability_domain        = local.my_ads[1]["name"]
  security_list_ids          = [oci_core_security_list.private.id]
  route_table_id             = oci_core_route_table.web_app_route.id
}

resource "oci_core_subnet" "lb_subnet" {
  vcn_id              = oci_core_vcn.web_apps_vcn.id
  compartment_id      = var.compartment_ocid
  display_name        = "LBSubnet"
  cidr_block          = local.third_subnet
  availability_domain = local.my_ads[2]["name"]
  security_list_ids   = [oci_core_security_list.private.id]
  route_table_id      = oci_core_route_table.web_app_route.id
}
