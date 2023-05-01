
# Zscaler Private Access Bulk Application Publish

This script will allow you to publish bulk application segments on your Zscaler Tenant.



## Features

- Publish multiple application segments
- Publish multiple domains and ports with one run



## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`export ZPA_CL_ID='Zscaler Client ID'`

`export ZPA_SC='Zscaler Secret Key`


## Setting up Zscaler Tenant and Customer ID under the auth.py

```python
import requests
import os

tenant = 'config.beta.zscalernode.com'
customer_id = '720641202XXXXXX'
```

## Importing tenant, customer id and access header from auth.py
```python
import requests
import json
import csv
from auth import tenant, customer_id, access_header


url = f"https://{tenant}/mgmtconfig/v1/admin/customers/{customer_id}"
```

## Setting up the CSV Payload. The payload should be named applicationsegments.csv.
```csv
Name,Domains,segmentGroup,TCP Ports,serverGroup
PROD.TEST.Segment1,TEST1.domain.corp,TEST.SegmentGroup,"80,8080","Local-Server,Remote-Server"
PROD.TEST.Segment2,TEST2.domain.corp,TEST.SegmentGroup,80,"Local-Server,Remote-Server"
```

## Running the script

```bash
python3 <scriptname>.py
```
## Notes

#### Segment/Server groups used by the script should already exist.


## Authors

- [@Clarence R. Subia](https://www.github.com/meliodaaf)


## References

[ZPA API](https://help.zscaler.com/zpa/api-reference)
