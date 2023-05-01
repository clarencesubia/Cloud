provider "oci" {
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
  region           = var.region
}

data "oci_core_shapes" "test_shapes" {
  compartment_id = var.compartment_ocid
  filter {
    name   = "name"
    values = ["VM.Standard2.1"]
  }
}

data "oci_core_images" "test_images" {
  compartment_id           = var.compartment_ocid
  sort_by                  = "TIMECREATED"
  sort_order               = "DESC"
  operating_system         = "Canonical Ubuntu"
  operating_system_version = "18.04 Minimal"
  shape                    = local.myshape
}


resource "oci_core_instance" "test_instance" {
  availability_domain = local.myad
  compartment_id      = var.compartment_ocid
  shape               = local.myshape
  display_name        = "StudentAC-VM1"

  create_vnic_details {
    subnet_id = oci_core_subnet.test_subnet.id
  }

  source_details {
    source_id   = local.myimage
    source_type = "image"
  }
}