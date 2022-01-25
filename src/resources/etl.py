from typing import List

import yfinance as yf
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from pandas import DataFrame

from resources.config import Config
from resources.time_it import time_it


@time_it
def extract_data(config: Config) -> DataFrame:
    df = yf.download(**config.yahoo_params)
    df.reset_index(inplace=True)
    return df


@time_it
def parse_data(data: DataFrame, ticker: str) -> List[Point]:
    return [Point('stocks') \
                .tag('ticker', ticker) \
                .field('open', record['Open']) \
                .field('high', record['High']) \
                .field('low', record['Low']) \
                .field('close', record['Close']) \
                .field('adj_close', record['Adj Close']) \
                .field('volume', record['Volume']) \
                .time(record['Date'])
            for record in data.to_dict('records')]


@time_it
def load_data(config: Config, data: DataFrame) -> None:
    tickers = config.yahoo_params.get('tickers')
    write_api = config.client.write_api(write_options=SYNCHRONOUS)
    if isinstance(tickers, str):
        datapoint_list = parse_data(data, tickers)
        write_api.write(bucket=config.BUCKET, org=config.ORG, record=datapoint_list)
    elif isinstance(tickers, list):
        for ticker in tickers:
            datapoint_list = parse_data(data, ticker)
            write_api.write(bucket=config.BUCKET, org=config.ORG, record=datapoint_list)


@time_it
def read_data(config: Config, query: str = None) -> None:
    query_api = config.client.query_api()
    query = query or 'from(bucket:"{0}") |> range(start: -{1})'.format(
        config.BUCKET, config.read_params['start_range'])
    tables = query_api.query(query)
    for table in tables:
        print('=> TABLE: ', table)
        for row in table.records:
            print('=> ROW: ', row.values)
