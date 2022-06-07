# kusto2csv

Download large Kusto queries one day at a time

# Environment Variables (put in .env file)
* KUSTO_CLUSTER
* KUSTO_APP_CLIENT_ID
* KUSTO_APP_CLIENT_SECRET
* KUSTO_APP_AUTHORITY_ID
* KUSTO_DB

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