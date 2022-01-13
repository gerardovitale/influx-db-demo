import os

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

ORG = os.environ.get('INFLUXDB_INIT_ORG')
BUCKET = os.environ.get('INFLUXDB_INIT_BUCKET')
TOKEN = os.environ.get('INFLUXDB_INIT_ADMIN_TOKEN')
URL = "http://influxdb:8086"

if __name__ == "__main__":
    print('[INFO] Executing: ', __name__)

    client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)
    write_api.write(bucket=BUCKET, org=ORG, record=p)

    print("[INFO] Execution's finished")
