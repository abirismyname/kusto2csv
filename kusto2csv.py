#!/usr/bin/env python3
import os
import argparse
from datetime import date
from time import sleep
from dateutil.rrule import rrule, DAILY
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
load_dotenv() 

from azure.kusto.data import (
    KustoClient, 
    KustoConnectionStringBuilder)
from azure.kusto.data.helpers import dataframe_from_result_table
CLUSTER = f'https://{os.getenv("KUSTO_CLUSTER")}.kusto.windows.net'
CLIENT_ID = os.getenv('KUSTO_APP_CLIENT_ID',"NA")
CLIENT_SECRET = os.getenv('KUSTO_APP_CLIENT_SECRET',"NA")
AUTHORITY_ID = os.getenv('KUSTO_APP_AUTHORITY_ID',"NA")
KUSTO_DB = os.getenv('KUSTO_DB',"NA")

parser = argparse.ArgumentParser(
    description='Download large Kusto queries one day at a time')
parser.add_argument('query_file', help='The KQL query file to run', default='query.kql')
parser.add_argument('-s', '--start', help='The start date')
parser.add_argument('-e', '--end', help='The end date')

args = parser.parse_args()

start_date = date.fromisoformat(args.start)
end_date = date.fromisoformat(args.end)

query_path = Path(args.query_file)
query = query_path.read_text()

try:
    kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(CLUSTER, CLIENT_ID, CLIENT_SECRET, AUTHORITY_ID)
    client = KustoClient(kcsb)
except Exception as ex:
    raise Exception('Error retrieving Kusto client object\n' + str(ex))

dfs = []
for dt in rrule(DAILY, dtstart=start_date, until=end_date):
    date_string = dt.strftime("%Y-%m-%d")
    print(f'Downloading data for {date_string}')
    
    response = client.execute_streaming_query(
        KUSTO_DB, 
        query.replace("$DATE", date_string))
    result = next(response.iter_primary_results())
    df = dataframe_from_result_table(result)

    output_file = query_path.parent / f'{query_path.stem}-{date_string}.csv'
    df.to_csv(output_file, index=False)

    sleep(2) # hack around timeouts

