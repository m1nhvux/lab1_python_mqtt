from datetime import datetime
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1884
TOPIC = "iot/lab/message"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Da ket noi broker. Dang cho tin nhan...")
        client.subscribe(TOPIC)
    else:
        print("Ket noi that bai:", reason_code)


def on_message(client, userdata, message):
    print("\nNhan duoc message:")
    print("Topic:", message.topic)
    print("Payload:", message.payload.decode("utf-8"))
    print("Time:", datetime.now().strftime("%H:%M:%S"))


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nDa dung subscriber")
finally:
    client.disconnect()