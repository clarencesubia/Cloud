## Zscaler Private Access Application Segment Creation Tool

This script allows you to publish application segments in ZPA (Zscaler Private Access) using a CSV or Excel file containing the segment details.

## Prerequisites
Before running the script, ensure you have the following:

- Python 3.x installed on your system
- Required Python libraries: argparse, requests
- ZPA client ID and client secret environment variables (ZPA_CL_ID and ZPA_SC)

```bash
pip3 install -r requirements.txt
```


## Usage
```bash
python3 ZpaAppSegment.py --file <CSV_FILE> --tenant <TENANT_NAME> --customer-id <CUSTOMER_ID>
```

Replace <CSV_FILE> with the path or name of the CSV file containing the segment details. The CSV file should have the following columns: Name, Domains, segmentGroup, serverGroup, TCP Ports.

Replace <TENANT_NAME> with the name of your ZPA tenant.

Replace <CUSTOMER_ID> with your ZPA customer ID.

For example:

```bash
python3 ZpaAppSegment.py apply --file segments.csv --tenant mytenant --customer-id 12345
```

## Retrieve Existing Application Segments Only
```bash
python3 ZpaAppSegment.py show --tenant mytenant --customer-id 12345
```

Description
The script performs the following actions:

- Parses the command-line arguments using argparse to retrieve the CSV file, tenant name, and customer ID.
- Authenticates with ZPA using the provided tenant name and customer ID.
- Creates an instance of ZpaApplicationManager to manage the application segments.
- Retrieves the name-to-ID bindings for segment groups and server groups.
- Publishes the application segments specified in the CSV file.
- Displays the status of each application segment creation.


## CSV File Format
The CSV file should have the following format:
```csv
Name,Domains,segmentGroup,serverGroup,TCP Ports,UDP Ports
Segment1,domain1.com,domain_group1,server_group1,80-81,3389
Segment2,domain2.com,domain_group2,server_group2,443,53
```

- Name: The name of the application segment.
- Domains: Comma-separated list of domain names associated with the segment.
- segmentGroup: The name of the segment group to which the segment belongs.
- serverGroup: Comma-separated list of server groups associated with the segment.
- TCP Ports: Comma-separated list of TCP/UDP ports accessible by the segment. Ranges can be specified using a dash, e.g., 80-81.


## API Reference
[ZPA API Reference Guide](https://help.zscaler.com/zpa/about-zpa-api)


## License
This script is licensed under the MIT License.

Please note that this script is provided as-is and without warranty. Use it at your own risk.
