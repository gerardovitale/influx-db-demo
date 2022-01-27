echo "==> building docker image influx-app"
docker build --rm -f Dockerfile -t influx-app .

echo ""
echo "==> running docker container influx-app"
docker run --rm \
  --name=influx-app \
  --network=influx-db-demo_default \
  -e INFLUXDB_INIT_ORG=organization \
  -e INFLUXDB_INIT_BUCKET=initialBucket \
  -e INFLUXDB_INIT_ADMIN_TOKEN=thisShouldBeSecret \
  influx-app
