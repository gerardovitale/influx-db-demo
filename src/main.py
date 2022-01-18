from resources.config import Config
from resources.etl import extract_data, load_data, read_data
from resources.time_it import ct

PARAMS = {
    'yahoo_tickers': 'TSLA',
    'yahoo_period': '5y',
    'yahoo_interval': '1d',
    'query_start_range': '5d',
}

cfg = Config(PARAMS)


def run_demo(config: Config) -> None:
    print('[INFO] {0} Executing: {1}'.format(ct(), __name__))

    data = extract_data(config=cfg)
    load_data(config=cfg,  data=data)

    print('[INFO] {0} Data loaded into InfluxDB'.format(ct()))

    read_data(config=cfg)
    cfg.client.close()

    print("[INFO] {0} Execution's finished".format(ct()))


if __name__ == "__main__":
    run_demo(config=cfg)
