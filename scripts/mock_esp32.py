import time
import random
import json
import paho.mqtt.client as mqtt
from datetime import datetime

MQTT_BROKER = "localhost"  # Change to your broker address if needed
MQTT_PORT = 1883
MQTT_TOPIC = "logs/app"

MACHINE_IDS = ["fan_01", "fan_02", "fan_03"]
STATES = ["normal", "anomalo"]

def random_log():
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "machine_id": random.choice(MACHINE_IDS),
        "estado": random.choice(STATES),
        "distancia": round(random.uniform(0.5, 1.5), 3)
    }

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_start()

try:
    while True:
        log = random_log()
        client.publish(MQTT_TOPIC, json.dumps(log))
        print(f"Published: {log}")
        time.sleep(random.uniform(1, 5))
except KeyboardInterrupt:
    print("Simulation stopped.")
finally:
    client.loop_stop()
    client.disconnect()
