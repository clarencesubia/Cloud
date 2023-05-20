// Gateways
resource "oci_core_internet_gateway" "ig" {
  compartment_id = var.compartment_ocid
  display_name   = "IG"
  vcn_id         = oci_core_vcn.web_apps_vcn.id
}

resource "oci_core_route_table" "web_app_route" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.web_apps_vcn.id
  display_name   = "WebApps-RT"
  route_rules {
    destination       = local.null_destination
    network_entity_id = oci_core_internet_gateway.ig.id
  }
}

resource "oci_core_route_table" "db_route" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.db_vcn.id
  display_name   = "DB-RT"
  route_rules {
    destination       = oci_core_vcn.web_apps_vcn.cidr_block
    network_entity_id = oci_core_local_peering_gateway.db_local_peering_gateway.id
  }
}

resource "oci_core_route_table" "app_route" {
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.web_apps_vcn.id
  display_name   = "App-RT"
  route_rules {
    destination       = oci_core_vcn.db_vcn.cidr_block
    network_entity_id = oci_core_local_peering_gateway.app_local_peering_gateway.id
  }
}


resource "oci_core_local_peering_gateway" "db_local_peering_gateway" {
  #Required
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.db_vcn.id
  peer_id        = oci_core_local_peering_gateway.app_local_peering_gateway.id
}

resource "oci_core_local_peering_gateway" "app_local_peering_gateway" {
  #Required
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.web_apps_vcn.id
}