import oci
import ipaddress


class Vcn:
    def __init__(self, config, compartment_id, vcn_display_name, cidr_block):
        self.config = config
        self.compartment_id = compartment_id
        self.vcn_display_name = vcn_display_name
        self.vcn_client = oci.core.VirtualNetworkClient(self.config)
        self.cidr_block = ipaddress.IPv4Network(cidr_block)
        self.subnetworks = list(self.cidr_block.subnets())
        self.vcn_data = {}


    def create_vcn(self):
        vcn_details = oci.core.models.CreateVcnDetails(
            cidr_block=str(self.cidr_block),
            display_name=self.vcn_display_name,
            compartment_id=self.compartment_id
        )
        vcn_response = self.vcn_client.create_vcn(create_vcn_details=vcn_details)
        self.vcn_data["vcn_id"] = vcn_response.data.id
        return vcn_response
        

    def create_internet_gateway(self):
        ig_details = oci.core.models.CreateInternetGatewayDetails(
            display_name=f"{self.vcn_display_name}-IG",
            compartment_id=self.compartment_id,
            is_enabled=True,
            vcn_id=self.vcn_data["vcn_id"]
        )
        ig_response = self.vcn_client.create_internet_gateway(create_internet_gateway_details=ig_details)
        self.vcn_data["ig_id"] = ig_response.data.id
        return ig_response


    def create_route_table(self):
        route_table_details = oci.core.models.CreateRouteTableDetails(
            compartment_id=self.compartment_id,
            display_name=f"{self.vcn_display_name}-RT",
            vcn_id=self.vcn_data["vcn_id"],
            route_rules=[
                oci.core.models.RouteRule(
                    network_entity_id=self.vcn_data["ig_id"],
                    cidr_block="0.0.0.0/0"
                    )
            ]
        )
        route_table_response = self.vcn_client.create_route_table(create_route_table_details=route_table_details)
        return route_table_response


    def create_security_list(self):
        sec_list_details = oci.core.models.CreateSecurityListDetails(
            compartment_id=self.compartment_id,
            display_name=f"{self.vcn_display_name}-SecList",
            vcn_id=self.vcn_data["vcn_id"],
            egress_security_rules=[
                oci.core.models.EgressSecurityRule(
                    destination="8.8.8.8/32",
                    protocol="6",
                    destination_type="CIDR_BLOCK",
                    is_stateless=False,
                    tcp_options=oci.core.models.TcpOptions(
                        destination_port_range=oci.core.models.PortRange(
                            max=8080,
                            min=8080
                            ),
                        ),
                    description="Python Created SecRule")
                ],
            ingress_security_rules=[
                oci.core.models.IngressSecurityRule(
                    protocol="6",
                    source="112.210.231.217/32",
                    is_stateless=False,
                    source_type="CIDR_BLOCK",
                    tcp_options=oci.core.models.TcpOptions(
                        destination_port_range=oci.core.models.PortRange(
                            max=80,
                            min=80
                            )
                        ),
                    description="Python Created Rule")
            ]
        )
        sec_list_response = self.vcn_client.create_security_list(create_security_list_details=sec_list_details)
        self.vcn_data["sec_list"] = sec_list_response.data.id
        return sec_list_response


    def create_subnet(self, public=True):
        subnet_details = oci.core.models.CreateSubnetDetails(
            compartment_id=self.compartment_id,
            display_name=f"{self.vcn_display_name}-Subnet-1",
            vcn_id=self.vcn_data["vcn_id"],
            cidr_block=str(self.subnetworks[1]),
            security_list_ids = [
                    self.vcn_data["sec_list"]
                ],
            prohibit_public_ip_on_vnic=public
        )
        subnet_response = self.vcn_client.create_subnet(create_subnet_details=subnet_details)
        return subnet_response


