variable "tenancy_ocid" {
  description = "OCI Tenancy to deploy to"
  type        = string
}

variable "compartment_ocid" {
  description = "OCI Compartment to deploy to"
  type        = string
  validation {
    condition     = can(regex("xyhxa$", var.compartment_ocid))
    error_message = "You are in the wrong comparment."
  }
}

variable "user_ocid" {
  description = "Identity of the user to use for provisioning"
  type        = string
}

variable "fingerprint" {
  description = "Fingerprint of API key to use for provisioning"
  sensitive   = true
}

variable "private_key_path" {
  description = " Path to API key to use for provisioning"
  type        = string
}

variable "region" {
  description = "OCI Region to deploy to"
  type        = string
}

variable "ssh_public_key_file" {
  description = "Pub Key"
  type        = string
}