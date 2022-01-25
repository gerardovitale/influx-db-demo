# InfluxDB Demo

This repository corresponds to a influxDB demo. It basically consists in a docker-compose with two services:
1. InfluxDB, to store timeseries data
2. Python App, which would download data, load it into the database and perform some basic queries

The demo was designed using Docker and Python.

## Requirements
- Docker installed and running on your local machine, and
- docker-compose package installed.

## Running the Demo
The code is structured to just type the following command from the root of the project:

```shell
$ docker-compose up --detach
```

The command above not only pull, build and deploy the docker containers services included in the docker-compose,
but also execute the 
[main.py](https://github.com/gerardovitale/influx-db-demo/blob/main/src/main.py) 
on the app service because this is included as an entrypoint in the 
[Dockerfile](https://github.com/gerardovitale/influx-db-demo/blob/main/Dockerfile#L31).

Next, if at the time it's interesting to consult the logs of any container (influxdb or app), run the following:

```shell
$ docker-compose logs -f <service-name>
```

At this point, the code should have been executed, so influxdb is up and running, and you could go onto
```http://localhost:8086```, and follow the instructions below to create/import a new chart:
1. Enter *user* and *password* corresponding defined in the docker-compose ENV variables,
2. Click on *"Build a Dashboard"*,
3. Click on *"Create Dashboard"* --> *"Import Dashboard"*,
4. At this point you could either load or copy-paste the dashboard-templates/tsla.json file.
5. Lastly, click on the name of the new dashboard icon that appeared on the screen and enjoy the view.

Finally, to end the demo and stop the containers just execute the following docker-compose command:

```shell
$ docker-compose stop
```

## Setup
In the case of setting up influxDB, it's needed the following ENV variables either in the 
[docker-compose.yml](https://github.com/gerardovitale/influx-db-demo/blob/main/docker-compose.yaml#L11-L17)
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

On the other hand, the python app needs to know DOCKER_INFLUXDB_INIT_ORG, DOCKER_INFLUXDB_INIT_BUCKET and 
DOCKER_INFLUXDB_INIT_ADMIN_TOKEN in order to establish a connection with the database throughout the client. 
This is done by passing this values also in the 
[docker-compose.yml](https://github.com/gerardovitale/influx-db-demo/blob/main/docker-compose.yaml#L30-L33);
however, this could be done by defining some constant variables with the corresponding values.

```yaml
# service -> app
environment:
    - INFLUXDB_INIT_ORG=organization
    - INFLUXDB_INIT_BUCKET=initialBucket
    - INFLUXDB_INIT_ADMIN_TOKEN=thisShouldBeSecret
```

## Developing or Contributing
In order to work with the docker-compose environment and test the features, it's recommended to execute
the command below, always from the project root. In my opinion, this is the easiest way to test and run many times as 
wanted the code and ensure the container or services included in the docker-compose rebuild and update with the 
changes done.

```shell
$ docker-compose build
$ docker-compose up --detach
```

Then, to consult the logs of the app container running execute the line below:

```shell
$ docker-compose logs -f app
```

And last, as it was shown before, run the following to stop every container:

```shell
$ docker-compose stop
```
