echo "=> building images"
dokcer-compose build --parallel

echo "=> running the docker-compose"
docker-compose up --detach

echo "=> getting the logs of influx-app container"
docker-compose logs -f influx-app