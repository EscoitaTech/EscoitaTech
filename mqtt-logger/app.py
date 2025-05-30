import time
import json
import random
import sys
import paho.mqtt.client as mqtt

# MQTT logger: generates random logs and publishes them to a MQTT broker

# Broker configuration
MQTT_BROKER = "localhost"  # Service name in docker-compose
MQTT_PORT = 1883
MQTT_TOPIC = "logs/app"

# Create MQTT client (no extra args to avoid deprecation warnings)
client = mqtt.Client()

try:
    # Connect to the MQTT broker
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    print("✅ Connected to MQTT broker", flush=True)
except Exception as e:
    print(f"❌ Error connecting to broker: {e}", flush=True)
    sys.exit(1)

# Simulated log levels
log_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]

def generate_log():
    """Generate a random log message with timestamp, level, and message."""
    level = random.choice(log_levels)
    return {
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "level": level,
        "message": f"Simulated log message ({level})",
        "source": "app-logger"
    }

# Main loop: publish a log every 5 seconds
while True:
    try:
        log = generate_log()
        payload = json.dumps(log)
        result = client.publish(MQTT_TOPIC, payload)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            print(f"⚠️ Error publishing message: {result}", flush=True)
        else:
            print(f"📤 Published: {payload}", flush=True)
        time.sleep(5)
    except Exception as e:
        print(f"❌ Error in main loop: {e}", flush=True)
        time.sleep(5)
