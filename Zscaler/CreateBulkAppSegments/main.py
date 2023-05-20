#!/usr/bin/env python3

import os
import sys
import csv

import argparse
import pandas as pd

from modules.ZpaAppSegment import Colors
from modules.ZpaAppSegment import ZpaAuthenticator
from modules.ZpaAppSegment import ZpaApplicationManager


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
