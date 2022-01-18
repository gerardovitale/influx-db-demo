import os
from typing import Dict

from influxdb_client import InfluxDBClient


class Config:
    ORG = os.environ.get('INFLUXDB_INIT_ORG')
    BUCKET = os.environ.get('INFLUXDB_INIT_BUCKET')
    TOKEN = os.environ.get('INFLUXDB_INIT_ADMIN_TOKEN')
    URL = "http://influxdb:8086"

    def __init__(self, params: Dict[str, str]):
        self.client = InfluxDBClient(url=self.URL, token=self.TOKEN, org=self.ORG)
        self.yahoo_params = {'tickers': params.get('yahoo_tickers', 'TSLA'),
                             'period': params.get('yahoo_period', '5y'),
                             'interval': params.get('yahoo_interval', '1d'),
                             }
        self.read_params = {'start_range': params.get('query_start_range', '5d'),
                            }
