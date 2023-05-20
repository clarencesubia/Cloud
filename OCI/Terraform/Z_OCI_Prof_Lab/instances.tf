locals {
  myshape = distinct(data.oci_core_shapes.test_shapes.shapes[*].name)[0]
  myimage = data.oci_core_images.test_images.images[0].id
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
  operating_system         = "Oracle Linux"
  operating_system_version = "8"
  shape                    = local.myshape
}

data "template_file" "user_data" {
  template = file("./cloud-init.yml")
}

resource "oci_core_instance" "vm_instances" {
  count               = 2
  availability_domain = local.my_ads[0]["name"]
  compartment_id      = var.compartment_ocid
  shape               = local.myshape
  display_name        = "WebServer-TF-${count.index}"
  metadata = {
    ssh_authorized_keys = "${file(var.ssh_public_key_file)}"
    user_data           = "${base64encode(data.template_file.user_data.rendered)}"
  }

  create_vnic_details {
    subnet_id        = oci_core_subnet.web_subnet.id
    assign_public_ip = true
    nsg_ids          = [oci_core_network_security_group.tf_network_security_group.id]
  }

  source_details {
    source_id   = local.myimage
    source_type = "image"
  }
}

resource "oci_core_instance" "db_instances" {
  availability_domain = local.my_ads[0]["name"]
  compartment_id      = var.compartment_ocid
  shape               = local.myshape
  display_name        = "DB-Instance-1"
  metadata = {
    ssh_authorized_keys = "${file(var.ssh_public_key_file)}"
    user_data           = "${base64encode(data.template_file.user_data.rendered)}"
  }

  create_vnic_details {
    subnet_id        = oci_core_subnet.db_subnet.id
    assign_public_ip = true
  }

  source_details {
    source_id   = local.myimage
    source_type = "image"
  }
}

resource "oci_core_instance" "app_instances" {
  availability_domain = local.my_ads[1]["name"]
  compartment_id      = var.compartment_ocid
  shape               = local.myshape
  display_name        = "App-Instance-1"
  metadata = {
    ssh_authorized_keys = "${file(var.ssh_public_key_file)}"
    user_data           = "${base64encode(data.template_file.user_data.rendered)}"
  }

  create_vnic_details {
    subnet_id        = oci_core_subnet.apps_subnet.id
    assign_public_ip = false
  }

  source_details {
    source_id   = local.myimage
    source_type = "image"
  }
}