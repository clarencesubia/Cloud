import argparse
import requests

import os
import csv
import json

class Colors():
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[36m'
    LIGHTCYAN = "\033[96m"
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class ZpaAuthenticator:
    def __init__(self, tenant, customer_id):
        self.tenant = tenant
        self.customer_id = customer_id
        self.auth_url = f"https://{self.tenant}/signin"

        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        self.client_id = os.environ.get("ZPA_CL_ID")
        self.client_secret = os.environ.get("ZPA_SC")
        self.payload = f"client_id={self.client_id}&client_secret={self.client_secret}"
        
        self.access_token = None
        self.access_header = None
        self.session = None


    def authenticate(self):
        self.session = requests.Session()
        response = requests.post(self.auth_url, headers=self.headers, data=self.payload).json()
        self.access_token = response["access_token"]
        self.access_header = {"Content-type": "application/json", "Authorization": f"Bearer {self.access_token}"}
        self.session.headers.update(self.access_header)



class ZpaApplicationManager(ZpaAuthenticator):
    def __init__(self, tenant, customer_id, payload_file):
        super().__init__(tenant, customer_id)
        self.payload_file = payload_file
        self.base_url = f"https://{tenant}/mgmtconfig/v1/admin/customers/{customer_id}"

        self.segment_group_ids = {}
        self.server_group_ids = {}
        self.authenticate()
        

    def get_group_bindings(self, group_type):
        print(f"{Colors.GREEN}{Colors.BOLD}Generating {str(group_type).upper()} Name to ID bindings.{Colors.END}")
        response = self.session.get(f"{self.base_url}/{group_type}Group?page=1&pagesize=500").json()
        data = response["list"]
        
        for item in data:
            groupName = item["name"]
            groupID = item["id"]

            if group_type == "segment":
                self.segment_group_ids[groupName] = groupID
            elif group_type == "server":
                self.server_group_ids[groupName] = groupID


    def add_app_segments(self):
        with open(self.payload_file, "r") as payload:
            applications = csv.DictReader(payload)

            for row in applications:
                name = row["Name"]
                domains = row["Domains"].split(",")
                segmentGroup = row["segmentGroup"]
                serverGroups = row["serverGroup"].split(",")
                servergroups = []
                for serverGroup in serverGroups:
                    svrgroupid = {"id": self.server_group_ids[serverGroup]}
                    servergroups.append(svrgroupid)

                tcp_ports = []
                if t_ports := row["TCP Ports"].split(","):
                    for port in t_ports:
                        if "-" in port:
                            port_range = port.split("-")
                            tcp_port = {"from": port_range[0], "to": port_range[1]}
                            if tcp_port not in tcp_ports:
                                tcp_ports.append(tcp_port)
                        else:
                            tcp_port = {"from": port, "to": port}
                            if tcp_port not in tcp_ports:
                                tcp_ports.append(tcp_port)

                udp_ports = []
                if u_ports := row["UDP Ports"].split(","):
                    for port in u_ports:
                        if "-" in port:
                            port_range = port.split("-")
                            udp_port = {"from": port_range[0], "to": port_range[1]}
                            if udp_port not in udp_ports:
                                udp_ports.append(udp_port)
                        else:
                            udp_port = {"from": port, "to": port}
                            if udp_port not in udp_ports:
                                udp_ports.append(udp_port)

                payload = json.dumps(
                    {
                        "name": name,
                        "enabled": "true",
                        "healthCheckType": "DEFAULT",
                        "healthReporting": "ON_ACCESS",
                        "icmpAccessType": "PING",
                        "passiveHealthEnabled": "true",
                        "ipAnchored": "false",
                        "doubleEncrypt": "false",
                        "bypassType": "NEVER",
                        "isCnameEnabled": "true",
                        "tcpPortRange": tcp_ports,
                        "udpPortRange": udp_ports,
                        "domainNames": domains,
                        "applicationGroupId": self.segment_group_ids[segmentGroup],
                        "serverGroups": servergroups
                    }
                )

                response = self.session.post(f'{self.base_url}/application', data=payload)
                if response.status_code == 201:
                    print(f"{Colors.GREEN}{Colors.BOLD}Application Segment {name}{Colors.END} - Created Successfully!")
                else:
                    print(f"{Colors.YELLOW}{Colors.BOLD}[!] Something went wrong:{Colors.END} {json.loads(response.text)['reason']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish Application Segments")
    parser.add_argument("--file", "-f", metavar="", help="CSV File Path or Name")
    parser.add_argument("--tenant", "-t", metavar="", help="ZPA Tenant Name")
    parser.add_argument("--customer-id", "-c", metavar="", help="ZPA Customer ID")
    args = parser.parse_args()

    file = args.file
    tenant = args.tenant
    customer_id = args.customer_id

    ZpaAuthenticator(tenant=tenant, customer_id=customer_id).authenticate()
    app_manager = ZpaApplicationManager(tenant=tenant, customer_id=customer_id, payload_file=file)

    app_manager.get_group_bindings(group_type="segment")
    app_manager.get_group_bindings(group_type="server")
    app_manager.add_app_segments()
