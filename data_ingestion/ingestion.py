import os
import time
import requests
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# Cấu hình
JSON_FILE_PATH = "/app/data_Crawl/landing_zone/fahasa_data.json" 


class JsonFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Kiểm tra nếu sự kiện không phải là thư mục và file chính là JSON_FILE_PATH
        if not event.is_directory and os.path.abspath(event.src_path) == os.path.abspath(JSON_FILE_PATH):
            print(f"File JSON thay đổi: {event.src_path} vào lúc {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            process_json_file()

def process_json_file():
    try:
        # Đọc file JSON
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # xóa dữ liệu
        delete_all_dochoi()
        # Gửi dữ liệu qua API
        send_to_api(transform_json(data))
        
    except json.JSONDecodeError as e:
        print(f"File {JSON_FILE_PATH} không phải là JSON hợp lệ: {e}")
    except Exception as e:
        print(f"Lỗi khi xử lý file JSON: {str(e)}")
        
def delete_all_dochoi(api_url="http://mysql_apifahasa:8002/dochoi"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.delete(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Dữ liệu đã được xóa thành công: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {e}")

def send_to_api(data_list, api_url="http://mysql_apifahasa:8002/dochoi"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(api_url, json=data_list, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"Dữ liệu đã được gửi thành công: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gửi dữ liệu đến API: {e}")
        
def transform_json(input_data):
    transformed_data = []
    for item in input_data:
        try:
            # Xử lý các trường số một cách an toàn
            price = item.get("price", "0")
            final_price = item.get("final_price", "0")
            discount_percent = item.get("discount_percent", "0")

            # Chuyển đổi sang float trước, sau đó thành int
            gia_goc = int(float(price)) if price and str(price).replace(".", "").isdigit() else 0
            gia_ban = int(float(final_price)) if final_price and str(final_price).replace(".", "").isdigit() else 0
            giam_gia = int(float(discount_percent)) if discount_percent and str(discount_percent).replace(".", "").isdigit() else 0

            transformed_item = {
                "id": str(item.get("id", item.get("product_id", ""))),
                "ten": str(item.get("name_a_title", item.get("name_a_label", ""))),
                "giaGoc": gia_goc,
                "giaBan": gia_ban,
                "giamGia": giam_gia,
                "hinh": str(item.get("image_src", "")),
                "doTuoiSD": "Không xác định",
                "namSX": 2024,
                "noiSX": "Không xác định",
                "moTa": "Không có mô tả",
                "kichThuoc": "Không xác định"
            }
            transformed_data.append(transformed_item)
        except (ValueError, TypeError) as e:
            print(f"Lỗi khi xử lý mục {item.get('id', 'unknown')}: {e}")
            continue
    return transformed_data

def main():
    # Kiểm tra xem file có tồn tại không
    if not os.path.exists(JSON_FILE_PATH):
        print(f"File {JSON_FILE_PATH} không tồn tại. Vui lòng tạo file trước khi giám sát.")
        return
    
    # Khởi tạo watchdog
    event_handler = JsonFileHandler()
    observer = Observer()
    
    # Theo dõi thư mục chứa file JSON
    watch_dir = os.path.dirname(JSON_FILE_PATH) or "."  # Nếu không có thư mục, theo dõi thư mục hiện tại
    observer.schedule(event_handler, path=watch_dir, recursive=False)
    observer.start()
    
    print(f"Bắt đầu theo dõi file: {JSON_FILE_PATH}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Dừng theo dõi...")
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    main()