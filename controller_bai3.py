from threading import Event
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1884
CMD_TOPIC = "iot/lab/light01/cmd"
STATUS_TOPIC = "iot/lab/light01/status"

ready = Event()


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        client.subscribe(STATUS_TOPIC)
    else:
        print("Ket noi that bai:", reason_code)


def on_subscribe(client, userdata, mid, reason_codes, properties):
    ready.set()


def on_message(client, userdata, message):
    print("\nTrang thai nhan duoc:")
    print(message.payload.decode("utf-8"))


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect(BROKER, PORT)
client.loop_start()

try:
    if not ready.wait(timeout=10):
        raise RuntimeError("Khong dang ky duoc topic trang thai")

    while True:
        command = input("Nhap lenh ON/OFF/EXIT: ").strip().upper()

        if command == "EXIT":
            break
        if command not in ("ON", "OFF"):
            print("Chi duoc nhap ON hoac OFF")
            continue

        result = client.publish(CMD_TOPIC, command)
        result.wait_for_publish()
        print("Da gui lenh", command)
finally:
    client.disconnect()
    client.loop_stop()