#!/usr/bin/python3

import requests
import json
import csv
from auth import tenant, customer_id, access_header


url = f"https://{tenant}/mgmtconfig/v1/admin/customers/{customer_id}"


session = requests.Session()
session.headers.update(access_header)


segmentGroupIDs = {}
serverGroupIDs = {}

def main():

    getGroupIdBindings(url, 'segment')
    getGroupIdBindings(url, 'server')
    addApplicationSegments(url)


def getGroupIdBindings(url, group):
    print(f"[*] Getting {str.capitalize(group)} ID Mapping.")
    response = session.get(f"{url}/{group}Group?page=1&pagesize=500").json()
    data = response["list"]
    
    for item in data:
        groupName = item["name"]
        groupID = item["id"]

        if group == "segment":
            segmentGroupIDs[groupName] = groupID
        elif group == "server":
            serverGroupIDs[groupName] = groupID


def addApplicationSegments(url):
    print("\n[+] Adding new Application Segment(s).\n")
    with open("applicationsegments.csv") as csv_file:
        applications = csv.DictReader(csv_file)

        for row in applications:
            name = row["Name"]
            domains = row["Domains"].split(",")
            segmentGroup = row["segmentGroup"]
            serverGroups = row["serverGroup"].split(",")
            servergroups = []
            for serverGroup in serverGroups:
                svrgroupid = {"id": serverGroupIDs[serverGroup]}
                servergroups.append(svrgroupid)
            ports = row["TCP Ports"].split(",")
            tcp_ports = []
            for port in ports:
                if "-" in port:
                    port = port.split("-")
                    tcp_port = {"from": port[0], "to": port[1]}
                    if tcp_port not in tcp_ports:
                        tcp_ports.append(tcp_port)
                else:
                    tcp_port = {"from": port, "to": port}
                    if tcp_port not in tcp_ports:
                        tcp_ports.append(tcp_port)

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
                    "domainNames": domains,
                    "applicationGroupId": segmentGroupIDs[segmentGroup],
                    "serverGroups": servergroups
                }
            )
            response = session.post(f'{url}/application', data=payload)

            if response.status_code == 201:
                print("HTTP Response OK " + response.status_code)
            else:
                print(f"[x] Something went wrong! {json.loads(response.text)['reason']}")



if __name__ == '__main__': main()