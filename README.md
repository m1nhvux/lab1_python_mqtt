# Thực hành buổi 1: Lập trình Python với MQTT

**Sinh viên:** Vũ Đình Ngọc Minh  
**Mã sinh viên:** B23DCCN569 

**Sinh viên:** Nguyễn Vũ Song Hà 
**Mã sinh viên:** B23DCCN265

Repo này gồm ba bài thực hành MQTT: gửi và nhận thông điệp, mô phỏng cảm biến nhiệt độ và độ ẩm, và điều khiển đèn thông minh. Mỗi bài có hai chương trình Python giao tiếp qua một MQTT broker.

## 1. Môi trường và cấu trúc thư mục

- Windows, Python 3.x.
- Thư viện Python: `paho-mqtt`.
- MQTT broker: Eclipse Mosquitto 

```text
BTH1/
├── README.md
├── mosquitto-lab.conf
├── publisher_bai1.py
├── subscriber_bai1.py
├── sensor_publisher_bai2.py
├── monitor_subscriber_bai2.py
├── device_bai3.py
└── controller_bai3.py
```

## 2. Cấu hình và chạy MQTT broker

1. Tải bộ cài Mosquitto dành cho Windows tại <https://mosquitto.org/download/> và cài đặt. Nếu đã cài Mosquitto thì bỏ qua bước này.
2. Tạo file `mosquitto-lab.conf` tại thư mục gốc của repo với nội dung:

   ```conf
   listener 1884 127.0.0.1
   allow_anonymous true
   ```

   `listener 1884 127.0.0.1` cho broker lắng nghe tại `localhost:1884`, chỉ nhận kết nối từ cùng máy. `allow_anonymous true` cho phép các chương trình của bài thực hành kết nối không cần tài khoản. Sử dụng cổng `1884`.

3. Mở PowerShell tại thư mục gốc của repo và chạy:

   ```powershell
   & "C:\Program Files\mosquitto\mosquitto.exe" -c ".\mosquitto-lab.conf" -v
   ```

   Nếu cài Mosquitto ở vị trí khác, thay đường dẫn đến `mosquitto.exe`. `-c` nạp file cấu hình, `-v` hiển thị log. Khi thấy `Opening ipv4 listen socket on port 1884` và `mosquitto version ... running`, giữ cửa sổ này mở trong lúc thực hành.

Các chương trình Python trong repo kết nối tới **host `localhost`, port `1884`**. Khi kết thúc, dừng tiến trình broker trong cửa sổ đã chạy nó.

## 3. Chuẩn bị Python và làm bài

1. Mở thư mục repo bằng IDE bất kì
2. Mở Terminal  tại thư mục repo, cài thư viện:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install paho-mqtt
   ```

   Nếu project chưa có `.venv`, tạo bằng `py -m venv .venv` rồi chạy lại lệnh cài đặt trên.

Mỗi bài cần **hai chương trình chạy đồng thời**. Có thể mở hai tab Terminal và chạy lệnh tương ứng bên dưới. Luôn khởi động broker ở mục 2 trước. Mỗi dòng lệnh trong một cặp phải chạy ở **một Terminal riêng**, không chạy nối tiếp trong cùng Terminal đang bị chương trình đầu tiên chiếm dụng.

## 4. Bài 1: Gửi và nhận thông điệp

**Topic:** `iot/lab/message`.

Chạy subscriber trước ở Terminal thứ nhất:

```powershell
.\.venv\Scripts\python.exe subscriber_bai1.py
```

Chạy publisher ở Terminal thứ hai:

```powershell
.\.venv\Scripts\python.exe publisher_bai1.py
```

Nhập lời chào ở publisher, ví dụ `hello`. Publisher ghép lời chào với mã sinh viên và họ tên rồi gửi lên topic. Subscriber in topic, payload và thời điểm nhận. Có thể nhập nhiều lời chào; nhập `EXIT` để thoát publisher.

**Kết quả đã quan sát ở publisher:**

```text
Da gui: hello - B23DCCN569 - Vu Dinh Ngoc Minh
Da gui: hihi - B23DCCN569 - Vu Dinh Ngoc Minh
```

**Kết quả cần kiểm tra ở subscriber:** mỗi thông điệp gửi khi subscriber đang chạy sẽ hiện `Topic: iot/lab/message`, `Payload: ...` và `Time: ...`. Tin gửi trước khi subscriber đăng ký topic sẽ không tự hiện lại.

## 5. Bài 2: Mô phỏng cảm biến nhiệt độ và độ ẩm

**Topic:** `iot/lab/sensor01/data`.

Chạy monitor trước ở Terminal thứ nhất:

```powershell
.\.venv\Scripts\python.exe monitor_subscriber_bai2.py
```

Chạy sensor ở Terminal thứ hai:

```powershell
.\.venv\Scripts\python.exe sensor_publisher_bai2.py
```

Sensor gửi dữ liệu JSON mỗi 3 giây, gồm `device_id`, `temperature` và `humidity`. Monitor đọc JSON và hiển thị thông tin. Nếu nhiệt độ **> 35 °C**, monitor in `CANH BAO: Nhiet do cao`. Nếu độ ẩm **< 40%**, monitor in `CANH BAO: Do am thap`. Hai điều kiện độc lập nên có thể xuất hiện đồng thời.

Ví dụ payload:

```json
{"device_id": "sensor01", "temperature": 36.1, "humidity": 38.7}
```

Đây là **định dạng và kết quả mong đợi**; các giá trị ngẫu nhiên thay đổi sau mỗi lần gửi.

## 6. Bài 3: Điều khiển đèn thông minh

| Topic | Chức năng |
| --- | --- |
| `iot/lab/light01/cmd` | Controller gửi lệnh `ON` hoặc `OFF` cho thiết bị. |
| `iot/lab/light01/status` | Thiết bị phản hồi trạng thái mới bằng JSON. |

Chạy thiết bị trước ở Terminal thứ nhất:

```powershell
.\.venv\Scripts\python.exe device_bai3.py
```

Chạy controller ở Terminal thứ hai:

```powershell
.\.venv\Scripts\python.exe controller_bai3.py
```

Nhập `ON` hoặc `OFF` trong controller. Thiết bị nhận lệnh từ topic `cmd`, đổi trạng thái và gửi phản hồi lên topic `status`. Controller nhận và in phản hồi. Ví dụ trạng thái mong đợi sau lệnh `ON`:

```json
{"device_id": "light01", "status": "ON"}
```

Nhập `EXIT` để thoát controller. Nếu nhập lệnh khác `ON`/`OFF`/`EXIT`, chương trình báo lệnh không hợp lệ.

## 7. Kiểm tra nhanh khi không nhận được dữ liệu

1. Broker vẫn đang chạy và log cho thấy nó lắng nghe cổng `1884`.
2. Cả hai chương trình dùng `localhost` và cổng `1884`.
3. Chương trình nhận hoặc thiết bị đã chạy **trước** khi gửi tin hay lệnh.
4. Topic ở phía gửi và phía nhận phải giống hệt nhau, kể cả chữ hoa và chữ thường.

