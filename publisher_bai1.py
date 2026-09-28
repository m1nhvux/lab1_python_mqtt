import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1884
TOPIC = "iot/lab/message"

HO_TEN = "Vu Dinh Ngoc Minh"
MA_SV = "B23DCCN569"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)
client.loop_start()

try:
    while True:
        loi_chao = input("Nhap loi chao (EXIT de thoat): ").strip()

        if loi_chao.upper() == "EXIT":
            break
        if not loi_chao:
            continue

        payload = f"{loi_chao} - {MA_SV} - {HO_TEN}"
        result = client.publish(TOPIC, payload)
        result.wait_for_publish()
        print("Da gui:", payload)
finally:
    client.disconnect()
    client.loop_stop()