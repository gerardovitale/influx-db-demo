from typing import List

import yfinance as yf
from influxdb_client import Point, InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from pandas import DataFrame

from resources.config import Config
from resources.time_it import time_it


@time_it
def extract_data() -> DataFrame:
    df = yf.download(**Config.YAHOO_PARAMS)
    df.reset_index(inplace=True)
    return df


@time_it
def parse_data(df: DataFrame) -> List[Point]:
    return [Point('stocks') \
                .tag('ticker', Config.YAHOO_PARAMS['tickers']) \
                .field('open', record['Open']) \
                .field('high', record['High']) \
                .field('low', record['Low']) \
                .field('close', record['Close']) \
                .field('adj_close', record['Adj Close']) \
                .field('volume', record['Volume']) \
                .time(record['Date'])
            for record in df.to_dict('records')]


@time_it
def load_data(client: InfluxDBClient, data: DataFrame) -> None:
    write_api = client.write_api(write_options=SYNCHRONOUS)
    datapoint_list = parse_data(data)
    write_api.write(bucket=Config.BUCKET, org=Config.ORG, record=datapoint_list)


@time_it
def read_data(client: InfluxDBClient, query: str = None) -> None:
    query_api = client.query_api()
    query = query or 'from(bucket:"{0}") |> range(start: -{1})'.format(
        Config.BUCKET, Config.QUERY_RANGE)
    tables = query_api.query(query)
    for table in tables:
        print('=> TABLE: ', table)
        for row in table.records:
            print('=> ROW: ', row.values)
