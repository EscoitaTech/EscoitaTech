# EscoitaTech Project Infrastructure

This folder contains the resources and configuration needed for the project infrastructure. Here you will find the key services and files for deployment and monitoring:

## Structure

- **docker/**
  - `docker-compose.yaml`: Service orchestration with Docker Compose.
  - **grafana/**
    - `dashboards/`: JSON dashboards for Grafana visualization.
    - `provisioning/`:
      - `contact-points/`: Alert configuration (Discord, Telegram).
      - `dashboards/`: Dashboards for automatic provisioning.
      - `datasources/`: Data source configuration for Grafana.
  - **mosquitto/**
    - `config/`: MQTT broker configuration (`mosquitto.conf`).
  - **telegraf/**
    - `telegraf.conf`: Telegraf configuration for metrics collection.

## Description

- **Grafana**: Monitoring and visualization of metrics and logs.
- **Mosquitto**: MQTT broker for device and service communication.
- **Telegraf**: Agent to collect and send metrics to InfluxDB.
- **Docker Compose**: Allows you to launch all services together in a reproducible way.

## Usage

1. Review and adapt the configurations for your environment.
2. Use `docker-compose.yaml` to start the services:
   ```sh
   docker-compose up -d
   ```
3. Connect to influxdb and generate a new token with the minimal permissions:
  3.1. Bucket `logs` with read and write
  3.2. Telegraf with read and write

4. Copy the api token and replace in the config related to the following services:
  4.1. Grafana: [datasources.yaml](docker\grafana\provisioning\datasources\datasources.yaml?plain=1#L17)
  4.2. Telegraf: [telegraf.conf](docker\telegraf\telegraf.conf?plain=1#L18)
  4.3. InfluxDB: [docker-compose.yaml](docker\docker-compose.yaml?plain=1#L27)

Access Grafana to view dashboards and metrics.

## Services and How to Connect

When running `docker-compose up -d`, the following local services are started:

- **Mosquitto (MQTT Broker)**
  - Host: `localhost:1883`
  - Connection: Any MQTT client can connect using port 1883. Example:
    - Broker URL: `mqtt://localhost:1883`

- **InfluxDB**
  - Host: `localhost:8086`
  - Web interface: [http://localhost:8086](http://localhost:8086)
  - User: `admin` | Password: `admin123`
  - Organization: `my-org` | Bucket: `logs`
  - Token: (see INFLUXDB_TOKEN variable in docker-compose.yaml)

- **Telegraf**
  - Metrics collection service. Does not expose a port directly, but connects to Mosquitto and InfluxDB internally.

- **Grafana**
  - Host: `localhost:3000`
  - Web interface: [http://localhost:3000](http://localhost:3000)
  - User: `admin` | Password: `admin`
  - Dashboards and alerts are automatically provisioned.

You can access each service from your browser or compatible tools using the hosts and credentials above.

## Connection Examples

### Mosquitto (MQTT Broker)
With `mosquitto_sub` and `mosquitto_pub`:

```sh
# Subscribe to a topic
mosquitto_sub -h localhost -p 1883 -t "test/topic"

# Publish a message
mosquitto_pub -h localhost -p 1883 -t "test/topic" -m "Hello MQTT"
```

### InfluxDB
Web access: [http://localhost:8086](http://localhost:8086)

With the InfluxDB CLI:

```sh
# List buckets
influx bucket list --host http://localhost:8086 --token <INFLUXDB_TOKEN>
```

### Grafana
Web access: [http://localhost:3000](http://localhost:3000)
User: `admin` | Password: `admin`

### Telegraf
No exposed port, but you can check container logs:

```sh
docker logs telegraf
```

## Data Simulation with mock.py

In the `/scripts/` folder you have a Python script to simulate blower machines and generate test data.

See the full documentation and usage instructions in the [scripts README](../scripts/README.md) and the [detailed simulation README](../scripts/mock_README.md).
### Telegraf
No expone puerto, pero puedes revisar logs del contenedor:

```sh
docker logs telegraf
```