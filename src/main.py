import os
from datetime import datetime

import influxdb_client
import yfinance as yf
from influxdb_client.client.write_api import SYNCHRONOUS
from pandas import DataFrame

ORG = os.environ.get('INFLUXDB_INIT_ORG')
BUCKET = os.environ.get('INFLUXDB_INIT_BUCKET')
TOKEN = os.environ.get('INFLUXDB_INIT_ADMIN_TOKEN')
URL = "http://influxdb:8086"

YAHOO_PARAMS = {
    'tickers': 'TSLA',
    'period': '5y',
    'interval': '1d',
}
QUERY_PARAMS = {
    'start_range': '5d',
}


def time() -> str:
    return datetime.now().isoformat()


if __name__ == "__main__":
    print('[INFO] {0} Executing: {1}'.format(time(), __name__))

    # InfluxDB Client
    client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    query_api = client.query_api()

    # Extract Data from Yahoo Finance API
    data: DataFrame = yf.download(**YAHOO_PARAMS)
    data.reset_index(inplace=True)

    # Load dataset into InfluxDB
    datapoint_list = [influxdb_client.Point('stocks') \
                          .tag('market', 'NASDAQ') \
                          .tag('ticker', YAHOO_PARAMS['tickers']) \
                          .field('open', record['Open']) \
                          .field('high', record['High']) \
                          .field('low', record['Low']) \
                          .field('close', record['Close']) \
                          .field('adj_close', record['Adj Close']) \
                          .field('volume', record['Volume']) \
                          .time(record['Date'])
                      for record in data.to_dict('records')]

    write_api.write(bucket=BUCKET, org=ORG, record=datapoint_list)

    print('[INFO] {0} Data loaded into InfluxDB'.format(time()))

    # Consult data from InfluxDB
    tables = query_api.query('from(bucket:"{0}") |> range(start: -{1})'.format(
        BUCKET, QUERY_PARAMS['start_range']))
    for table in tables:
        print('=> TABLE: ', type(table), table)
        for row in table.records:
            print('=> ROW: ', type(row.values), row.values)

    print("[INFO] {0} Execution's finished".format(time()))
