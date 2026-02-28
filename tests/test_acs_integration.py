import pytest
import time
from utils.acs_client import GenieACSClient
from utils.ssh_client import exec_ssh_command

def test_acs_set_and_gateway_verify(config):
    acs_cfg = config['genieacs']
    gateway = config['gateway']
    test_data = config['test_data']
    
    acs = GenieACSClient(acs_cfg)

    # BƯỚC 1: Set giá trị mới thông qua GenieACS API
    print(f"Setting {test_data['param_path']} to {test_data['new_value']} via GenieACS...")
    success = acs.set_parameter(test_data['param_path'], test_data['new_value'])
    assert success is True, "Không thể gửi task tới GenieACS"

    # BƯỚC 2: Chờ CWMP session hoàn tất (GenieACS đẩy xuống Gateway)
    # Trong môi trường Lab, thường mất 5-10s
    time.sleep(15)

    # BƯỚC 3: Truy vấn trực tiếp Data Model trên Gateway qua SSH (Backend)
    # PrplOS thường dùng amx-cli để quản lý TR-181
    check_cmd = f'amx-cli -g "{test_data["param_path"]}"'
    actual_value = exec_ssh_command(gateway['ip'], gateway['ssh_user'], gateway['ssh_pass'], check_cmd)

    print(f"Value on Gateway: {actual_value}")

    # Kiểm tra xem giá trị thực tế trên Gateway có khớp với giá trị đã set từ ACS không
    assert test_data['new_value'] in actual_value, \
        f"Data Model mismatch! ACS set: {test_data['new_value']}, Gateway has: {actual_value}"

def test_gateway_change_and_acs_refresh(config):
    # Kịch bản ngược lại: Đổi trên Gateway -> Refresh ACS -> Check ACS API
    # Thường dùng để test tính năng 'Inform' hoặc 'Get' của ACS
    pass

"""
GenieACS sử dụng REST API để tương tác với thiết bị.
Để thực hiện bài test này, framework của bạn sẽ đóng vai trò là tầng
Northbound Interface (NBI). Kịch bản sẽ là:

    Gọi API của GenieACS để ra lệnh Set/Get (CWMP).
    Chờ GenieACS đẩy cấu hình xuống Gateway qua giao thức TR-069.
    SSH vào Gateway để kiểm tra trực tiếp qua Data Model (amx-cli/ubus) xem giá trị đã thực sự thay đổi dưới Hardware chưa.
    
"""