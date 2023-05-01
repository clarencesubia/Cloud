#!/usr/bin/env python3

import oci
import argparse
from modules.VcnWizard import Vcn

parser = argparse.ArgumentParser(description="Creates VCN Infrastructure. Mimics the VCN Wizard in GUI.")
parser.add_argument("--vcn-name", required=True, help="VCN Name to be applied.", metavar="")
parser.add_argument("--cidr-block", required=True, help="CIRD block for the VCN to be created.", metavar="")
parser.add_argument("--region", help="The target region to be retrieved or deleted from.", metavar="")

args = parser.parse_args()

vcn_name = args.vcn_name
cidr_block = args.cidr_block
region = args.region

config = oci.config.from_file("~/.oci/config")
compartment_id = "ocid1.compartment.oc1..aaaaaaaa3a42xreobbzuk67xz47xsyo6drspaeftjb2wu5upzrrcirenwerq"

if __name__ == '__main__':
    vcn_ops = Vcn(
        config=config,
        compartment_id=compartment_id,
        vcn_display_name=vcn_name,
        cidr_block=cidr_block
    )
    vcn_ops.create_vcn()
    vcn_ops.create_internet_gateway()
    vcn_ops.create_route_table()
    vcn_ops.create_security_list()
    vcn_ops.create_subnet(public=True)
    

    
    
    
