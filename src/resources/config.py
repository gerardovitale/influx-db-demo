import os


class Config:
    ORG = os.environ.get('INFLUXDB_INIT_ORG')
    BUCKET = os.environ.get('INFLUXDB_INIT_BUCKET')
    TOKEN = os.environ.get('INFLUXDB_INIT_ADMIN_TOKEN')
    URL = "http://influxdb:8086"
    YAHOO_PARAMS = {
        'tickers': 'TSLA',
        'period': '5y',
        'interval': '1d',
    }
    QUERY_RANGE = '5d'
