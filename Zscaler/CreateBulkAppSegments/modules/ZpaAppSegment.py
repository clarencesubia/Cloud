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

        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        self.client_id = os.environ.get("ZPA_CL_ID")
        self.client_secret = os.environ.get("ZPA_SC")
        self.payload = f"client_id={self.client_id}&client_secret={self.client_secret}"
        
        self.access_token = None
        self.access_header = None
        self.session = None
        
    @property
    def auth_url(self):
        return f"https://{self.tenant}/signin"


    def authenticate(self):
        self.session = requests.Session()
        response = requests.post(self.auth_url, headers=self.headers, data=self.payload).json()
        self.access_token = response["access_token"]
        self.access_header = {"Content-type": "application/json", "Authorization": f"Bearer {self.access_token}"}
        self.session.headers.update(self.access_header)


class ZpaApplicationManager(ZpaAuthenticator):
    def __init__(self, tenant, customer_id, payload_file="", mode="apply"):
        super().__init__(tenant, customer_id)
        self.payload_file = payload_file

        self.segment_group_ids = {}
        self.server_group_ids = {}
        self.authenticate()

        self.mode = mode
        
    
    @property
    def base_url(self):
        return f"https://{self.tenant}/mgmtconfig/v1/admin/customers/{self.customer_id}"
        

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
                if t_ports := row["TCP Ports"]:
                    t_ports = t_ports.split(",")
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
                if u_ports := row["UDP Ports"]:
                    u_ports = u_ports.split(",")
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
                        "applicationGroupId": segmentGroup,
                        "serverGroups": serverGroups
                    }
                )

                if self.mode == "plan":
                    for line in payload:
                        name = line["name"]
                        domains = line["domainNames"]
                        tcpports = line["tcpPortRange"]
                        udpports = line["udpPortRange"]
                        segment_group = line["applicationGroupId"]
                        server_groups = line["serverGroups"]

                        print(f"{Colors.GREEN}\nSummary of the application segments that will be done:{Colors.END}")
                        print(f"Application Segment: {name}")
                        print(f"Domains/URLs: {domains}")
                        print(f"TCP Ports: {tcpports}")
                        print(f"UDP Ports: {udpports}")
                        print(f"Segment Group: {segment_group}")
                        print(f"Server Groups: {server_groups}")

                elif self.mode == "apply":
                    print(f"{Colors.GREEN}{Colors.BOLD}[!] Application Creation Mode:{Colors.END}")
                    response = self.session.post(f'{self.base_url}/application', data=payload)
                    if response.status_code == 201:
                        print(f"{Colors.GREEN}{Colors.BOLD}Application Segment {name}{Colors.END} - Created Successfully!")
                    else:
                        print(f"{Colors.YELLOW}{Colors.BOLD}[!] Something went wrong:{Colors.END} {json.loads(response.text)['reason']}")


    def list_application_segments(self):
        print(f"{Colors.GREEN}\nRetrieving existing application segments:{Colors.END}")
        output = []
        page_number = 1

        while True:
            try:
                print(f"[*] Retrieving apps from page {page_number}.")
                params = {"page": page_number, "pagesize": 500}
                response = self.session.get(f"{self.base_url}/application", params=params)
                data = json.loads(response.text)["list"]
                output.extend(data)
                page_number += 1
            except KeyError:
                print("Reached last page.")
                break

        for item in output:
            try:
                name = item["name"]
            except KeyError:
                name = None
            try:
                segment_group = item["segmentGroupName"]
            except KeyError:
                segment_group = None
            try:
                tcpports = ",".join(list(set(item["tcpPortRanges"])))
            except KeyError:
                tcpports = None
            try:
                udpports = ",".join(list(set(item["udpPortRanges"])))
            except KeyError:
                udpports = None
            try:
                domains = ",".join(item["domainNames"])
            except KeyError:
                domains = None
            try:
                sg = []
                server_groups = item["serverGroups"]
                for index, item in enumerate(server_groups):
                    sg.append(item["name"])
                sg = ",".join(sg)
            except KeyError:
                server_groups = None
            
            print(f"Application Segment: {name}")
            print(f"Domains/URLs: {domains}")
            print(f"TCP Ports: {tcpports}")
            print(f"UDP Ports: {udpports}")
            print(f"Segment Group: {segment_group}")
            print(f"Server Groups: {server_groups}")



