import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1884
CMD_TOPIC = "iot/lab/light01/cmd"
STATUS_TOPIC = "iot/lab/light01/status"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Thiet bi den da ket noi. Dang cho lenh...")
        client.subscribe(CMD_TOPIC)
    else:
        print("Ket noi that bai:", reason_code)


def on_message(client, userdata, message):
    command = message.payload.decode("utf-8").strip().upper()

    if command not in ("ON", "OFF"):
        print("Lenh khong hop le:", command)
        return

    status = {"device_id": "light01", "status": command}
    client.publish(STATUS_TOPIC, json.dumps(status))
    print("Da chuyen den sang", command)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nDa dung thiet bi")
finally:
    client.disconnect()