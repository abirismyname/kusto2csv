# kusto2csv

Download large Kusto/Azure Data Explorer queries one day at a time

# Environment Variables (put in .env file)
* KUSTO_CLUSTER - Full URL of Kusto cluster
* KUSTO_APP_CLIENT_ID - Kusto client ID
* KUSTO_APP_CLIENT_SECRET - Kusto client secret
* KUSTO_APP_AUTHORITY_ID - Kusto authority ID
* KUSTO_DB - Kusto database name

# Setup (Tested against python 3.7.11)
```
pip3 install -r requirements.txt 
```

# Usage
```
kusto2csv -s START_DATE -e END_DATE KQL_FILE
```

Example:
```
kusto2csv.py -s 2022-06-05 -e 2022-06-06 query.kql
```