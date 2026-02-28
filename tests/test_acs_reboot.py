import pytest
import time
from utils.acs_client import GenieACSClient
from utils.network import wait_for_reboot
from utils.ssh_client import exec_ssh_command

"""
Để test kịch bản
Reboot từ GenieACS, framework cần thực hiện: Gọi API Reboot từ ACS -> Kiểm tra Gateway mất kết nối (Ping) -> Đợi Gateway khởi động lại -> Kiểm tra uptime hoặc trạng thái trên Data Model.
"""

def test_genieacs_reboot_gateway(config):
    acs_cfg = config['genieacs']
    gateway = config['gateway']
    acs = GenieACSClient(acs_cfg)

    # BƯỚC 1: Lấy Uptime hiện tại qua SSH trước khi Reboot
    uptime_cmd = "cat /proc/uptime | cut -d' ' -f1"
    old_uptime = float(exec_ssh_command(gateway['ip'], gateway['ssh_user'], gateway['ssh_pass'], uptime_cmd))
    print(f"Uptime trước reboot: {old_uptime}s")

    # BƯỚC 2: Click "Reboot" thông qua GenieACS API
    success = acs.reboot_device()
    assert success is True, "Không thể gửi lệnh Reboot từ GenieACS"

    # BƯỚC 3: Monitor quá trình Reboot (Ping)
    is_rebooted = wait_for_reboot(gateway['ip'])
    assert is_rebooted is True, "Gateway không khởi động lại đúng hạn"

    # Đợi thêm một chút để các service (amx, ubus) sẵn sàng
    time.sleep(10)

    # BƯỚC 4: Verify Uptime mới trên Data Model
    # Uptime mới phải nhỏ hơn Uptime cũ
    new_uptime = float(exec_ssh_command(gateway['ip'], gateway['ssh_user'], gateway['ssh_pass'], uptime_cmd))
    print(f"Uptime sau reboot: {new_uptime}s")

    assert new_uptime < old_uptime, "Lỗi: Uptime không reset, có vẻ Gateway chưa thực sự Reboot"
    assert new_uptime < 300, "Lỗi: Uptime quá lớn sau khi Reboot"

    # BƯỚC 5: Verify trạng thái trên TR-181 (Ví dụ: Device.DeviceInfo.UpTime)
    # Lệnh amx-cli tùy biến theo prplOS
    tr181_uptime = exec_ssh_command(gateway['ip'], gateway['ssh_user'], gateway['ssh_pass'], 
                                   'amx-cli -g "Device.DeviceInfo.UpTime"')
    assert int(tr181_uptime) > 0


"""
Kịch bản này kết hợp ACS API, Ping Check và SSH Data Model để verify Uptime.

Điểm mấu chốt khi test Reboot:

    CWMP Session: Khi bạn gọi API Reboot, GenieACS sẽ chờ lần Inform tiếp theo (hoặc gửi Connection Request) để đẩy lệnh. Hãy đảm bảo Gateway đang Online và sẵn sàng nhận Connection Request.
    Graceful Reboot: PrplOS sẽ thực hiện các thủ tục đóng service trước khi restart, vì vậy wait_for_reboot cần có timeout đủ linh hoạt (thường 2-3 phút).
    Persistence: Sau khi Reboot, hãy check xem các cài đặt trước đó (như SSID đã set ở bài test trước) có bị mất không (Data Persistence Test).
"""