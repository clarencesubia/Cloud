resource "oci_core_vcn" "web_apps_vcn" {
  cidr_block     = local.web_app_cidr
  compartment_id = var.compartment_ocid
  display_name   = "WebAppsVCN"
}

resource "oci_core_vcn" "db_vcn" {
  cidr_block     = local.db_cidr
  compartment_id = var.compartment_ocid
  display_name   = "DBVCN"
}

resource "oci_core_subnet" "web_subnet" {
  vcn_id              = oci_core_vcn.web_apps_vcn.id
  compartment_id      = var.compartment_ocid
  display_name        = "WebSubnet"
  cidr_block          = local.first_subnet
  availability_domain = local.my_ads[0]["name"]
  security_list_ids   = [oci_core_security_list.private.id]
  route_table_id      = oci_core_route_table.web_app_route.id
}

resource "oci_core_subnet" "apps_subnet" {
  vcn_id                     = oci_core_vcn.web_apps_vcn.id
  compartment_id             = var.compartment_ocid
  display_name               = "AppsSubnet"
  cidr_block                 = local.second_subnet
  prohibit_public_ip_on_vnic = true
  availability_domain        = local.my_ads[1]["name"]
  security_list_ids          = [oci_core_security_list.private.id, oci_core_security_list.app_to_db.id]
  route_table_id             = oci_core_route_table.app_route.id
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

resource "oci_core_subnet" "db_subnet" {
  vcn_id              = oci_core_vcn.db_vcn.id
  compartment_id      = var.compartment_ocid
  display_name        = "DBSubnet"
  cidr_block          = local.db_subnet_1
  availability_domain = local.my_ads[0]["name"]
  security_list_ids   = [oci_core_security_list.db_to_apps.id]
  route_table_id      = oci_core_route_table.db_route.id
}