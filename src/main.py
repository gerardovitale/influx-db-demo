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
YAHOO_CONFIG = {
    'tickers': 'TSLA',
    'period': '5d',
    'interval': '1d',
}


def time() -> str:
    return datetime.now().isoformat()


if __name__ == "__main__":
    print('[INFO] {0} Executing: {1}'.format(time(), __name__))

    client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    query_api = client.query_api()

    data: DataFrame = yf.download(**YAHOO_CONFIG)
    data.reset_index(inplace=True)

    datapoint_list = []
    for record in data.to_dict('records'):
        datapoint = influxdb_client.Point('stocks') \
            .tag('market', 'NASDAQ').tag('ticker', YAHOO_CONFIG['tickers']) \
            .field('open', record['Open']).field('high', record['High']).field('low', record['Low']) \
            .field('close', record['Close']).field('adj_close', record['Adj Close']).field('volume', record['Volume']) \
            .time(record['Date'])
        datapoint_list.append(datapoint)
    write_api.write(bucket=BUCKET, org=ORG, record=datapoint_list)

    print('[INFO] {0} Data loaded into InfluxDB'.format(time()))

    tables = query_api.query('from(bucket:"{0}") |> range(start: -1y)'.format(BUCKET))
    for table in tables:
        print('=> TABLE: ', table)
        for row in table.records:
            print('=> ROW: ', row.values)

    print("[INFO] {0} Execution's finished".format(time()))
