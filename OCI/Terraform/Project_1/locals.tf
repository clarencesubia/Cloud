locals {
  myshape = distinct(data.oci_core_shapes.test_shapes.shapes[*].name)[0]
  myimage = data.oci_core_images.test_images.images[0].id
  myad = data.oci_identity_availability_domain.AD.name
}