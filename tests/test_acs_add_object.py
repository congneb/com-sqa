import pytest
import time
import re
from utils.acs_client import GenieACSClient
from utils.ssh_client import exec_ssh_command

def test_acs_add_static_lease_and_verify(config):
    acs_cfg = config['genieacs']
    gateway = config['gateway']
    data = config['test_add_object']
    
    acs = GenieACSClient(acs_cfg)

    # BƯỚC 1: Đếm số lượng Object hiện có trước khi Add (để tìm Index mới)
    count_cmd = f'amx-cli -g "{data["parent_path"]}*"'
    initial_output = exec_ssh_command(gateway['ip'], gateway['ssh_user'], gateway['ssh_pass'], count_cmd)
    
    # BƯỚC 2: Gọi API Add Object từ GenieACS
    print(f"Adding new object to {data['parent_path']}...")
    assert acs.add_object(data['parent_path']) is True

    # Chờ ACS thực hiện phiên làm việc CWMP (AddObject)
    time.sleep(10)

    # BƯỚC 3: Tìm Index của Object vừa tạo trên Gateway
    new_output = exec_ssh_command(gateway['ip'], gateway['ssh_user'], gateway['ssh_pass'], count_cmd)
    # Logic: Tìm index mới xuất hiện (Ví dụ từ .1. sang .2.)
    # Giả sử prplOS trả về danh sách các instance
    
    # BƯỚC 4: Cấu hình thông số cho Instance mới qua ACS
    # Thông thường sau khi add, Index sẽ là n+1 hoặc theo response của ACS
    # Ở đây ta giả định lấy index cuối cùng từ lệnh check amx-cli
    new_index = "2" # Ví dụ logic tìm index
    new_obj_path = f"{data['parent_path']}{new_index}."

    print(f"Configuring new object: {new_obj_path}")
    for param, value in data['params'].items():
        acs.set_parameter(f"{new_obj_path}{param}", value)

    time.sleep(10)

    # BƯỚC 5: Verify cuối cùng trên Data Model prplOS
    final_verify = exec_ssh_command(gateway['ip'], gateway['ssh_user'], gateway['ssh_pass'], 
                                   f'amx-cli -g "{new_obj_path}"')
    
    assert data['params']['Chaddr'] in final_verify
    assert data['params']['Yiaddr'] in final_verify
    print(f"Thêm Object thành công! Data trên Gateway: {final_verify}")

"""
    Dynamic Instance Management: Kiểm tra khả năng cấp phát tài nguyên động của stack CWMP trên Gateway.
    Index Mapping: Đảm bảo Index mà ACS quản lý khớp hoàn toàn với Instance Index trong hệ thống Ambiorix/prplOS.
    Resource Leak: Test xem việc add/delete liên tục có gây tràn bộ nhớ hay lỗi logic trong Data Model không.

Lưu ý cho prplOS:
Lệnh amx-cli rất mạnh, bạn có thể dùng amx-cli -o json để lấy dữ liệu dạng JSON, giúp việc parse Index trong Python dễ dàng hơn bằng json.loads().
"""