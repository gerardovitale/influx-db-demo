from influxdb_client import InfluxDBClient

from resources.config import Config
from resources.etl import extract_data, load_data, read_data
from resources.time_it import ct

if __name__ == "__main__":
    print('[INFO] {0} Executing: {1}'.format(ct(), __name__))

    client = InfluxDBClient(url=Config.URL, token=Config.TOKEN, org=Config.ORG)
    data = extract_data()
    load_data(client, data)

    print('[INFO] {0} Data loaded into InfluxDB'.format(ct()))

    read_data(client)
    client.close()

    print("[INFO] {0} Execution's finished".format(ct()))
