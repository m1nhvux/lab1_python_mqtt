import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1884
TOPIC = "iot/lab/sensor01/data"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Dang theo doi sensor01...")
        client.subscribe(TOPIC)
    else:
        print("Ket noi that bai:", reason_code)


def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode("utf-8"))
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])

        print(f"\nDevice: {data['device_id']}")
        print(f"Temperature: {temperature} C")
        print(f"Humidity: {humidity} %")

        if temperature > 35:
            print("CANH BAO: Nhiet do cao")
        if humidity < 40:
            print("CANH BAO: Do am thap")
    except (ValueError, KeyError, TypeError) as error:
        print("Du lieu khong hop le:", error)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nDa dung monitor")
finally:
    client.disconnect()