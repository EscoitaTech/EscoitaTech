# Grafana

This folder contains the configuration and resources for the Grafana monitoring service.

## Structure
- `dashboards/`: JSON dashboards for metrics and log visualization.
- `provisioning/`: Automatic provisioning configuration for Grafana.
  - `contact-points/`: Alert configuration (Discord, Telegram).
  - `dashboards/`: Dashboards for automatic provisioning.
  - `datasources/`: Data source configuration (InfluxDB, etc).

## Usage
Grafana is started with Docker Compose and is accessible at [http://localhost:3000](http://localhost:3000) (user: admin, password: admin).
Dashboards and alerts are automatically provisioned from this folder.

## How it works
- All dashboards in the `dashboards/` folder are loaded automatically on startup.
- Data sources and alert contact points are provisioned from the files in the `provisioning/` subfolders.

## More information
See the main infrastructure [README](../../README.md) for details on how to launch the stack and connect to Grafana.
