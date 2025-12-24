
# Hybrid LTE Gateway

📡 Chức năng chính của Hybrid LTE Gateway

    Kết nối Internet: kết hợp đường truyền cố định (cáp quang/DSL) với LTE/4G/5G để đảm bảo mạng liên tục.
    
    Failover & Load balancing: tự động chuyển sang LTE khi WAN mất, hoặc chia tải giữa hai đường truyền.
    
    Router/Gateway: cung cấp Wi-Fi, LAN cho nhiều thiết bị trong mạng nội bộ.

🖥️ 1. Kiểm thử phần cứng

    Khởi động thiết bị: thời gian boot, đèn báo trạng thái.
    
    Cổng kết nối: WAN (cáp quang/DSL), LTE (SIM), LAN, Wi-Fi, USB.
    
    SIM LTE/5G: nhận diện, tín hiệu, tốc độ.
    
    Nhiệt độ & nguồn điện: hoạt động ổn định khi chạy lâu, xử lý mất điện đột ngột.

📡 2. Kiểm thử kết nối mạng

    WAN cố định: tốc độ, độ ổn định khi dùng cáp quang/DSL.
    
    LTE/5G: tốc độ download/upload, độ trễ, khả năng roaming.
    
    Failover (chuyển đổi dự phòng): khi WAN mất, tự động chuyển sang LTE trong bao lâu.
    
    Load balancing (cân bằng tải): phân chia lưu lượng giữa WAN và LTE.
    
    Khả năng phục hồi: khi WAN trở lại, thiết bị có tự động chuyển lại không.

📲 3. Kiểm thử phần mềm & giao diện

    Web UI / App quản lý: đăng nhập, cấu hình, hiển thị trạng thái.
    
    Firmware update: OTA update, rollback khi lỗi.
    
    Quản lý SIM LTE: hiển thị dung lượng data, cảnh báo khi hết gói.
    
    Logs & monitoring: ghi nhận sự kiện, cảnh báo lỗi.

🔐 4. Kiểm thử bảo mật

    Xác thực người dùng: mật khẩu, tài khoản quản trị.
    
    Mã hóa dữ liệu: VPN, HTTPS, WPA2/WPA3 cho Wi-Fi.
    
    Firewall & NAT: kiểm tra chặn port, lọc IP.
    
    Tấn công giả lập: brute force, DDoS nhỏ, injection.

⚡ 5. Kiểm thử hiệu năng

    Throughput test: đo tốc độ tối đa WAN và LTE.
    
    Latency test: độ trễ khi chuyển đổi giữa WAN ↔ LTE.
    
    Stress test: chạy nhiều kết nối đồng thời, tải nặng trong nhiều giờ.
    
    QoS (Quality of Service): ưu tiên luồng dữ liệu (video, VoIP).

🌍 6. Kiểm thử tính năng nâng cao

    VPN client/server: kết nối và duy trì ổn định.
    
    Parental control: chặn website, lọc nội dung.
    
    Guest Wi-Fi: tạo mạng phụ, kiểm tra cách ly với mạng chính.
    
    IPv6 support: kiểm tra khả năng hoạt động song song IPv4/IPv6.

## Auto Test

### Kịch bản - Failover từ WAN sang LTE

```
import time
import requests

STB_IP = "192.168.1.100"
STB_PORT = 8080
BASE_URL = f"http://{STB_IP}:{STB_PORT}"

def get_status():
    resp = requests.get(f"{BASE_URL}/status")
    return resp.text if resp.status_code == 200 else None

def simulate_wan_down():
    resp = requests.get(f"{BASE_URL}/simulate_wan_down")
    return resp.status_code == 200

def verify_lte_active(timeout=10, interval=2):
    start = time.time()
    while time.time() - start < timeout:
        status = get_status()
        if status and "LTE_OK" in status:
            return True
        time.sleep(interval)
    return False

def test_failover():
    print("🔎 Kiểm tra trạng thái WAN...")
    status = get_status()
    assert "WAN_OK" in status, "WAN không hoạt động như mong đợi"

    print("⚡ Giả lập mất WAN...")
    assert simulate_wan_down(), "Không thể giả lập WAN down"

    print("⏳ Chờ chuyển sang LTE...")
    assert verify_lte_active(), "Failover sang LTE thất bại"

    print("✅ Test case Failover WAN → LTE thành công!")

if __name__ == "__main__":
    test_failover()

```

🛠️ Giải thích

    get_status(): gọi API /status để lấy trạng thái WAN/LTE.
    
    simulate_wan_down(): giả lập mất kết nối WAN.
    
    verify_lte_active(): chờ tối đa 10 giây, kiểm tra mỗi 2 giây để xác nhận LTE đã kích hoạt.
    
    test_failover(): chạy toàn bộ kịch bản và assert kết quả.

👉 Đây là skeleton script, bạn có thể mở rộng thêm:

    Load balancing test: đo tỷ lệ phân chia lưu lượng WAN/LTE.
    
    Recovery test: khi WAN trở lại, gateway tự động chuyển lại.
    
    Performance test: đo latency khi failover.

### Kịch bản - Load Balancing (WAN + LTE cùng lúc)

kiểm tra xem gateway có thực sự phân chia lưu lượng giữa WAN và LTE hay không.

```
import requests
import time

STB_IP = "192.168.1.100"
STB_PORT = 8080
BASE_URL = f"http://{STB_IP}:{STB_PORT}"

def get_status():
    resp = requests.get(f"{BASE_URL}/status")
    return resp.json() if resp.status_code == 200 else None

def send_traffic(source="WAN", duration=10):
    """Giả lập gửi lưu lượng qua WAN hoặc LTE"""
    resp = requests.get(f"{BASE_URL}/simulate_traffic?src={source}&duration={duration}")
    return resp.status_code == 200

def test_load_balancing():
    print("🔎 Kiểm tra trạng thái ban đầu...")
    status = get_status()
    assert status, "Không lấy được trạng thái thiết bị"
    print("Trạng thái:", status)

    print("⚡ Gửi lưu lượng qua WAN...")
    assert send_traffic("WAN", 10), "Không thể gửi traffic WAN"

    print("⚡ Gửi lưu lượng qua LTE...")
    assert send_traffic("LTE", 10), "Không thể gửi traffic LTE"

    print("⏳ Chờ thiết bị cân bằng tải...")
    time.sleep(5)

    status = get_status()
    print("📊 Trạng thái sau khi cân bằng:", status)

    # Kiểm tra tỷ lệ phân chia lưu lượng
    wan_usage = status.get("wan_usage", 0)
    lte_usage = status.get("lte_usage", 0)

    assert wan_usage > 0, "WAN không có lưu lượng"
    assert lte_usage > 0, "LTE không có lưu lượng"
    print(f"✅ Load balancing OK - WAN: {wan_usage} Mbps, LTE: {lte_usage} Mbps")

if __name__ == "__main__":
    test_load_balancing()

```

🛠️ Giải thích

      get_status(): gọi API /status để lấy thông tin WAN/LTE usage.
      
      send_traffic(): giả lập gửi lưu lượng qua WAN hoặc LTE.
      
      test_load_balancing(): gửi traffic song song, chờ thiết bị cân bằng tải, sau đó kiểm tra tỷ lệ phân chia.
      
      wan_usage / lte_usage: giả định API trả về thông số băng thông sử dụng.
