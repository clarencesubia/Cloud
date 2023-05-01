variable "tenancy_ocid" {
  description = "OCI Tenancy to deploy to"
  type        = string
  default     = "ocid1.tenancy.oc1..aaaaaaaanjxhtf43kfqmqsqk6u7lrlkywyyxiv7di2b2a34ez4x3n4yeluoa"
}

variable "compartment_ocid" {
  description = "OCI Compartment to deploy to"
  type        = string
  default     = "ocid1.compartment.oc1..aaaaaaaaozh6gasuvzyzvpta4cz6ryxjmd3e6qinko6l7pogh46bm25xyhxa"
}

variable "user_ocid" {
  description = "Identity of the user to use for provisioning"
  type        = string
  default     = "ocid1.user.oc1..aaaaaaaavfuwbkkefdmr6z4kr3xl6xdkpweimpga66whg3pwbji33lcmdfcq"
}

variable "fingerprint" {
  description = "Fingerprint of API key to use for provisioning"
  sensitive   = true
  default     = "4c:f2:74:75:9f:fc:a8:46:0d:88:c0:99:02:8e:0a:d9"
}

variable "private_key_path" {
  description = " Path to API key to use for provisioning"
  type        = string
  default     = "/home/ayens/.oci/clarence-subia.pem"
}

variable "region" {
  description = "OCI Region to deploy to"
  type        = string
  default     = "us-phoenix-1"
}