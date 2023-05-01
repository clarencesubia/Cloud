data "oci_core_services" "test_oci_services" {
  filter {
    name = "name"
    values = [".*Object.*Storage"]
    regex = true
  }
}