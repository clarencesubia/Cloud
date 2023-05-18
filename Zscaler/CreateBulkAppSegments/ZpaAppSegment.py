import argparse
import requests
import pandas as pd

import os
import csv
import sys
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
    def __init__(self, tenant, customer_id, payload_file="", mode="apply"):
        super().__init__(tenant, customer_id)
        self.payload_file = payload_file
        self.base_url = f"https://{tenant}/mgmtconfig/v1/admin/customers/{customer_id}"

        self.segment_group_ids = {}
        self.server_group_ids = {}
        self.authenticate()

        self.mode = mode
        

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



def normalize_payload(target_xlsx):
    print(f"{Colors.GREEN}{Colors.BOLD}[!] Converting XLSX file to CSV! {Colors.END}")
    try:
        xls = pd.ExcelFile(target_xlsx)
        app_segments = pd.read_excel(xls, "Application Segments")
    except FileNotFoundError as err:
        print(f"{Colors.YELLOW}{Colors.BOLD}{err}{Colors.END}")
        sys.exit()
    app_segments.to_csv(f"application_segments_raw.csv", index=None, header=True)
    
    with open(f"application_segments_raw.csv", "r") as csv_file:
        csvReader = csv.DictReader(csv_file)
        with open(f"application_segments.csv", "w") as csv_file:
            csvWriter = csv.writer(csv_file)
            header = ["Name", "Domains", "segmentGroup", "serverGroup", "TCP Ports", "UDP Ports"]
            csvWriter.writerow(header)
            for row in csvReader:
                    name = row["Name"].strip()
                    segmentGroup = row["segmentGroup"].strip()
                    domains = (
                        row["Domains"]
                        .strip()
                        .replace("\n", ",")
                        .replace(" ,", ",")
                        .replace("\t,", ",")
                    )
                    serverGroup = row["serverGroup"]
                    if tcpPorts := row["TCP Ports"]:
                        tcpPorts = tcpPorts.strip().replace("\n", ",").strip(".0")
                    if udpPorts := row["UDP Ports"]:
                        udpPorts = udpPorts.strip().replace("\n", ",").strip(".0")

                    output = name, domains, segmentGroup, serverGroup, tcpPorts, udpPorts
                    csvWriter.writerow(output)

    print(f"{Colors.GREEN}{Colors.BOLD}[!] Deleting file application_segments_raw.csv!{Colors.END}")
    if os.path.exists("application_segments_raw.csv"):
        os.remove("application_segments_raw.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish Application Segments")
    parser.add_argument("--tenant", "-t", metavar="", help="ZPA Tenant Name")
    parser.add_argument("--customer-id", "-c", metavar="", help="ZPA Customer ID")

    subparsers = parser.add_subparsers(help='Define run-mode as show, plan, apply', dest='command')

    apply = subparsers.add_parser("apply", help="Apply changes to create application segments.")
    apply.add_argument("--file", required=True, help="CSV or Excel File Path or Name")
    apply.add_argument("--show-only", help="Plan mode")

    show = subparsers.add_parser("show", help="Show existing application segments.")

    args = parser.parse_args()

    tenant = args.tenant
    command = args.command
    customer_id = args.customer_id
    show_only = args.show_only

    if command == "apply":
        if show_only:
            mode = "plan"

        file = args.file
        if ".xlsx" in file:
            normalize_payload(file)
            payload_file = "application_segments.csv"
        elif ".csv" in file:
            payload_file = file
        else:
            print(f"{Colors.RED}{Colors.BOLD}[!] Wrong file extension. Use .csv or .xlsx only!{Colors.END}")
            sys.exit(1)
        
        ZpaAuthenticator(tenant=tenant, customer_id=customer_id).authenticate()
        app_manager = ZpaApplicationManager(tenant=tenant, customer_id=customer_id, payload_file=payload_file, mode=mode)
        app_manager.add_app_segments()
        app_manager.get_group_bindings(group_type="segment")
        app_manager.get_group_bindings(group_type="server")
        app_manager.add_app_segments()

    elif command == "show":
        ZpaAuthenticator(tenant=tenant, customer_id=customer_id).authenticate()
        app_manager = ZpaApplicationManager(tenant=tenant, customer_id=customer_id)
        app_manager.list_application_segments()
