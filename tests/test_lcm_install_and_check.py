import pytest
import time
from utils.ssh_client import exec_ssh_command, check_system_logs

def test_lcm_install_with_log_verification(config):
    gateway = config['gateway']
    lcm_cfg = config['lcm']
    log_cfg = config['lcm_logs']
    
    # 1. Gửi lệnh cài đặt qua Data Model (amx-cli)
    install_cmd = f'amx-cli -g "Device.SoftwareModules.InstallDu(URL=\'{lcm_cfg["package_url"]}\')"'
    exec_ssh_command(gateway['ip'], gateway['ssh_user'], gateway['ssh_pass'], install_cmd)
    
    print("Đang chờ xử lý cài đặt và kiểm tra log...")
    
    # 2. Kiểm tra log hệ thống (Polling trong 30s)
    found_log = False
    for _ in range(6):
        time.sleep(5)
        # Kiểm tra xem có bản tin Notify của USP hoặc log thành công không
        found, full_log = check_system_logs(
            gateway['ip'], 
            gateway['ssh_user'], 
            gateway['ssh_pass'], 
            log_cfg['usp_notify']
        )
        
        if found:
            found_log = True
            print("Tìm thấy bản tin USP Notify trong hệ thống!")
            break
            
    assert found_log is True, f"Không tìm thấy bản tin Notify '{log_cfg['usp_notify']}' trong logread"

    # 3. Verify trạng thái cuối cùng của Data Model
    check_status = f'amx-cli -g "Device.SoftwareModules.DeploymentUnit.{lcm_cfg["package_name"]}.Status"'
    final_status = exec_ssh_command(gateway['ip'], gateway['ssh_user'], gateway['ssh_pass'], check_status)
    
    assert "Installed" in final_status
