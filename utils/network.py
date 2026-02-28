"""
Utility Kiểm tra Trạng thái Mạng (utils/network.py)
Dùng để xác nhận Gateway đã thực sự khởi động lại (mất kết nối tạm thời).
"""

import os
import time

def wait_for_reboot(ip, timeout=120):
    print(f"Đang chờ Gateway {ip} Reboot...")
    # 1. Chờ Gateway ngắt kết nối (Ping fail)
    start_time = time.time()
    while time.time() - start_time < 30:
        response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null")
        if response != 0:
            print("Gateway đã Down.")
            break
        time.sleep(2)
    
    # 2. Chờ Gateway Online trở lại (Ping success)
    start_time = time.time()
    while time.time() - start_time < timeout:
        response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null")
        if response == 0:
            print("Gateway đã Up trở lại.")
            return True
        time.sleep(5)
    return False
