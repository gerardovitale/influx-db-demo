# InfluxDB Demo

This repository corresponds to a influxDB demo. It basically consists in a docker-compose with two services:
1. InfluxDB, to store timeseries data
2. Python App, which would download data, load it into the database and perform some basic queries

The demo was designed using Docker and Python.

## Requirements
- Docker installed and running on your local machine.
- docker-compose package installed.

## Setup
In the case of setting up influxDB, it's needed the following ENV variables either in the 
[docker-compose.yml](https://github.com/gerardovitale/influx-db-demo/blob/main/docker-compose.yaml#L13-L19)
or when run the container:

```yaml
# service -> influxdb
environment:
    - DOCKER_INFLUXDB_INIT_MODE=setup
    - DOCKER_INFLUXDB_INIT_USERNAME=admin
    - DOCKER_INFLUXDB_INIT_PASSWORD=admin2021
    - DOCKER_INFLUXDB_INIT_ORG=organization
    - DOCKER_INFLUXDB_INIT_BUCKET=initialBucket
    - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=thisShouldBeSecret
```

On the other hand, the python app need to know DOCKER_INFLUXDB_INIT_ORG, DOCKER_INFLUXDB_INIT_BUCKET and 
DOCKER_INFLUXDB_INIT_ADMIN_TOKEN in order to establish a connection with the database throughout the client. 
This is done by passing this values also in the 
[docker-compose.yml](https://github.com/gerardovitale/influx-db-demo/blob/main/docker-compose.yaml#L32-L35);
however, this could be done by defining some constant variables with the corresponding values.

```yaml
# service -> app
environment:
    - INFLUXDB_INIT_ORG=organization
    - INFLUXDB_INIT_BUCKET=initialBucket
    - INFLUXDB_INIT_ADMIN_TOKEN=thisShouldBeSecret
```

## Running the Demo
The code is structured to just type the following command from the root of the project:

```shell
$ docker-compose up --detach
```

The command above not only pull, build and deploy the docker containers services included in the docker-compose,
but also execute the 
[main.py](https://github.com/gerardovitale/influx-db-demo/blob/main/src/main.py) 
on the app service because this is included as an entrypoint in the 
[Dockerfile](https://github.com/gerardovitale/influx-db-demo/blob/main/Dockerfile#L33).

Next, if at the time result interest to consult the logs of any container (influxdb or influx-app, run the following:

```shell
$ docker-compose logs -f <container-name>
```
Finally, to end the demo just execute the following:

```shell
$ docker-compose stop
```

## Developing or Contributing
In order to work with the docker-compose environment and test the features, it's recommended to execute
the command below, always from the project root. In my opinion, this is the easiest way to test and run many times as wanted the code and ensure the container or 
services included in the docker-compose rebuild and update with the changes done.

```shell
$ docker-compose build --parallel
$ docker-compose up --detach
```

Then, to consult the logs of the app container running execute the line below:

```shell
$ docker-compose logs -f influx-app
```

And last, as it was shown before, run the following to stop every container:

```shell
$ docker-compose stop
```
