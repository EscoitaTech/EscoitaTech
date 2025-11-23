# Telegraf

This folder contains the configuration for the Telegraf metrics agent.

## Structure
- `telegraf.conf`: Main configuration file for Telegraf.

## Usage
Telegraf is started with Docker Compose and automatically connects to Mosquitto and InfluxDB as configured. It does not expose an external port, but you can check its operation in the container logs.
