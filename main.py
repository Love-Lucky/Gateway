import time
import threading
import serial
import json
from Adafruit_IO import MQTTClient

class FaceAIGateway:
    def __init__(self):
        self.username = ""
        self.key = ""
        
        self.feeds = {
            "door": "smart-door-control",
            "light": "smart-light-control",
            "sensors": "environmental-data",
            "logs": "security-log"
        }

        self.client = MQTTClient(self.username, self.key)
        self.client.on_connect = self.on_connected
        self.client.on_disconnect = self.on_disconnected
        self.client.on_message = self.on_message
        
        self.serial_port = "COM1" # Thay bằng cổng thực tế
        self.baudrate = 115200 # Thay bằng cổng thực tế
        self.ser = serial.Serial(port="COM1", baudrate=115200, timeout=1)
        self.is_running = True

    def on_connected(self, client):
        print(">>> [MQTT] Connected. Subscribing to feeds...")
        for feed in self.feeds.values():
            client.subscribe(feed)

    def on_disconnected(self, client):
        print(">>> [MQTT] Warning: Connection lost. Retrying...")

    def on_message(self, client, feed_id, payload):
        """Xử lý lệnh từ Dashboard đẩy xuống thiết bị"""
        print(f">>> [Cloud Command] {feed_id}: {payload}")
        if self.ser and self.ser.is_open:
            command = f"!{feed_id.upper()}:{payload}#"
            self.ser.write(command.encode())

    def connect_serial(self):
        """Cơ chế tự động kết nối lại Serial"""
        while self.is_running:
            try:
                if not self.ser or not self.ser.is_open:
                    self.ser = serial.Serial(self.serial_port, self.baudrate, timeout=1)
                    print(f">>> [Serial] Connected to {self.serial_port}")
                time.sleep(5)
            except Exception as e:
                print(f">>> [Serial] Error: {e}. Retrying in 5s...")
                time.sleep(5)

    def read_serial_loop(self):
        """Luồng đọc dữ liệu cảm biến độc lập"""
        while self.is_running:
            if self.ser and self.ser.is_open and self.ser.in_waiting > 0:
                try:
                    raw_data = self.ser.readline().decode('utf-8').strip()
                    self.process_hardware_data(raw_data)
                except Exception as e:
                    print(f">>> [Serial] Read error: {e}")
            time.sleep(0.1)

    def process_hardware_data(self, data):
        """Bóc tách dữ liệu theo giao thức đã chốt với Hưng"""
        if data.startswith("!") and data.endswith("#"):
            payload = data[1:-1]
            print(f">>> [Hardware] Received: {payload}")
            self.client.publish(self.feeds["sensors"], payload)

    def start(self):
        serial_thread = threading.Thread(target=self.connect_serial, daemon=True)
        read_thread = threading.Thread(target=self.read_serial_loop, daemon=True)
        
        serial_thread.start()
        read_thread.start()
        
        print(">>> Gateway is running. Press Ctrl+C to stop.")
        self.client.connect()
        self.client.loop_blocking()

if __name__ == "__main__":
    gateway = FaceAIGateway()
    gateway.start()