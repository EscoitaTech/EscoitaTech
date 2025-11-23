# Mosquitto

This folder contains the configuration for the Mosquitto MQTT broker.

## Structure
- `config/`: Main configuration file (`mosquitto.conf`).

## Usage
Mosquitto is started with Docker Compose and exposes port 1883 locally. You can connect any MQTT client to `localhost:1883` using the configuration defined here.
