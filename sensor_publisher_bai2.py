import json
import random
import time
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1884
TOPIC = "iot/lab/sensor01/data"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)
client.loop_start()

try:
    while True:
        data = {
            "device_id": "sensor01",
            "temperature": round(random.uniform(25, 40), 1),
            "humidity": round(random.uniform(30, 75), 1),
        }

        payload = json.dumps(data)
        result = client.publish(TOPIC, payload)
        result.wait_for_publish()

        print("Da gui:", payload)
        time.sleep(3)
except KeyboardInterrupt:
    print("\nDa dung sensor")
finally:
    client.disconnect()
    client.loop_stop()