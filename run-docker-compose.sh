echo "=> building images"
docker-compose build

echo "=> running the docker-compose"
docker-compose up --detach