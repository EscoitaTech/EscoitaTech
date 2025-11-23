# Blower Machine Simulation with mock.py

This Python script simulates the operation of blower machines, generating random data and sending it to the MQTT broker configured in the infrastructure.

## What does it do?
- Publishes messages to the `logs/app` topic with the following fields:
  - `machine_id`: Machine identifier (fan_01, fan_02, fan_03)
  - `estado`: Machine state ("normal" or "anomalo")
  - `distancia`: Simulated numeric value between 0.5 and 1.5
  - `timestamp`: Date and time in UTC format

## Example published message
```json
{
  "timestamp": "2025-11-23T16:04:38.318439Z",
  "machine_id": "fan_03",
  "estado": "anomalo",
  "distancia": 1.283
}
```

## How to run the simulation

1. Go to the `scripts` folder:
   ```sh
   cd scripts
   ```
2. Create and activate a virtual environment:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the required dependency:
   ```sh
   pip install paho-mqtt
   ```
4. Run the script:
   ```sh
   python mock.py
   ```

This will generate simulated data that you can view in Grafana and query in InfluxDB.
