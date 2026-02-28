import pytest
import time
import json
from utils.acs_client import GenieACSClient
from utils.ssh_client import exec_ssh_command

def test_acs_delete_static_lease_and_verify(config):
    acs_cfg = config['genieacs']
    gateway = config['gateway']
    parent_path = config['test_add_object']['parent_path'] # Ví dụ: Device.DHCPv4.Server.Pool.1.StaticAddress.
    
    acs = GenieACSClient(acs_cfg)

    # BƯỚC 1: Tìm một Index đang tồn tại trên Gateway (Sử dụng -o json để parse dễ dàng)
    # Lệnh amx-cli trả về JSON giúp xác định chính xác các instance
    list_cmd = f'amx-cli -o json -g "{parent_path}*"'
    output_raw = exec_ssh_command(gateway['ip'], gateway['ssh_user'], gateway['ssh_pass'], list_cmd)
    
    # Giả sử output trả về list các path, ta lấy path đầu tiên để xóa
    # Lưu ý: Cần xử lý logic parse JSON tùy theo format output của prplOS/Ambiorix
    try:
        instances = json.loads(output_raw)
        if not instances:
            pytest.skip("Không tìm thấy Object nào để xóa.")
        
        # Lấy path của instance đầu tiên (ví dụ: Device.DHCPv4.Server.Pool.1.StaticAddress.1.)
        target_path = list(instances.keys())[0]
        if not target_path.endswith('.'): target_path += '.'
    except Exception:
        # Fallback nếu không parse được JSON (giả định xóa index 1)
        target_path = f"{parent_path}1."

    print(f"Tiến hành xóa Object: {target_path}")

    # BƯỚC 2: Gọi API Delete Object từ GenieACS
    assert acs.delete_object(target_path) is True

    # BƯỚC 3: Chờ CWMP session (DeleteObject) hoàn tất
    time.sleep(15)

    # BƯỚC 4: Verify trên Gateway qua SSH
    # Sử dụng lệnh amx-cli để check xem path đó còn tồn tại không
    verify_cmd = f'amx-cli -g "{target_path}"'
    final_output = exec_ssh_command(gateway['ip'], gateway['ssh_user'], gateway['ssh_pass'], verify_cmd)

    # Nếu xóa thành công, amx-cli thường trả về lỗi "Object not found" hoặc rỗng
    assert "not found" in final_output.lower() or final_output.strip() == ""
    print(f"Xóa thành công Object {target_path} khỏi Data Model.")

"""
Kịch bản này sẽ:

    Xác định một Object đang tồn tại trên Gateway.
    Ra lệnh xóa từ GenieACS.
    Kiểm tra xem Object đó còn xuất hiện trong Data Model của prplOS hay không.
    
GenieACS Sync: Sau khi xóa qua API, GenieACS sẽ tự động cập nhật lại cơ sở dữ liệu của nó sau phiên Inform tiếp theo.
"""