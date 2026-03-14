# FaceAI Smart Door - Gateway Module

## 1. Giới thiệu dự án
Dự án FaceAI Smart Door + Auto Lighting + Security Log tập trung vào việc xây dựng hệ thống nhà thông minh có khả năng mở khóa bằng nhận diện khuôn mặt, tự động hóa ánh sáng và ghi chép nhật ký an ninh.

Module Gateway đóng vai trò là "trạm trung chuyển" dữ liệu giữa:
- **Thiết bị (Yolo:Bit/Arduino):** Thu thập dữ liệu cảm biến và thực thi lệnh điều khiển (Servo/LED).
- **Trí tuệ nhân tạo (FaceAI):** Nhận diện người dùng và đưa ra quyết định mở khóa.
- **Cloud (Adafruit IO):** Hiển thị Dashboard và lưu trữ trạng thái hệ thống.

## 2. Các chức năng chính (Gateway Logic Code)
- **Bridge E2E:** Kết nối thông suốt 2 chiều Serial ↔ MQTT (Adafruit IO).
  - *Cloud to Hardware:* Nhận lệnh từ các feed (`smart-door-control`, `smart-light-control`, `environmental-data`, `security-log`) và chuyển tiếp xuống thiết bị qua Serial theo định dạng `!FEED_ID:VALUE#`.
  - *Hardware to Cloud:* Đọc dữ liệu từ cổng Serial theo định dạng `!VALUE#` và đẩy lên MQTT feed `environmental-data`.
- **Multithreading Process:** Chạy đa luồng độc lập gồm luồng xử lý MQTT, luồng giám sát Serial, và luồng lấy dữ liệu cảm biến liên tục. 
- **Network & Serial Stability:** Cơ chế tự động kết nối lại (Auto-reconnect) thông minh khi rớt mạng hoặc cáp vật lý (USB Serial) bị ngắt.

## 3. Yêu cầu hệ thống
- **Ngôn ngữ:** Python 3.x.
- **Thư viện cần thiết:**
  - `paho-mqtt`: Giao tiếp với Cloud Adafruit.
  - `pyserial`: Giao tiếp phần cứng qua cổng USB.
  - `adafruit-io`: Thư viện hỗ trợ API của Adafruit.

## 4. Hướng dẫn cài đặt và khởi chạy

**Cài đặt thư viện:**
```bash
pip install -r requirements.txt
```

**Cấu hình thông số:** 
Mở file `main.py` và cập nhật các cấu hình:
- **Adafruit IO Credentials:** Sửa thông tin tài khoản ở `self.username = "YOUR_USERNAME"` và `self.key = "YOUR_KEY"`.
- **Serial Port:** Cập nhật biến `self.serial_port` (VD: `COM3` trên Windows, hoặc `/dev/ttyUSB0` trên Linux/Mac).
- **Baudrate:** Theo mặc định là `115200`.

**Chạy Gateway:**
```bash
python main.py
```
