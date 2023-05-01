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