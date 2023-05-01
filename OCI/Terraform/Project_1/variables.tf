variable "tenancy_ocid" {}
variable "compartment_ocid" {}
variable "user_ocid" {}
variable "fingerprint" {
    sensitive = true
}
variable "private_key_path" {}
variable "region" {}