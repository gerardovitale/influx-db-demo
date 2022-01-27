echo "=> building images"
docker-compose build

echo ""
echo "=> running the docker-compose"
docker-compose up --detach

echo ""
echo "==> building docker image influx-app"
docker build --rm -f Dockerfile -t influx-app .

echo ""
echo "==> running docker container influx-app"

if [ $# -eq 0 ]; then
  echo "Using default Tickers"
else
  TICKERS=$1
fi

docker run --rm \
  --name=influx-app \
  --network=influx-db-demo_default \
  -e INFLUXDB_INIT_ORG=organization \
  -e INFLUXDB_INIT_BUCKET=initialBucket \
  -e INFLUXDB_INIT_ADMIN_TOKEN=thisShouldBeSecret \
  -e YAHOO_TICKERS="$TICKERS" \
  influx-app
