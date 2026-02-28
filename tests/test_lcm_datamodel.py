import pytest
import time
from utils.ssh_client import exec_ssh_command # Giả định bạn đã có hàm exec lệnh chung

def test_lcm_install_via_datamodel(config):
    gateway = config['gateway']
    lcm_cfg = config['lcm']
    
    # 1. Thực hiện lệnh Install qua amx-cli (Công cụ đặc trưng của prplOS)
    # Lệnh: Device.SoftwareModules.InstallDu(URL, UUID, Username, Password)
    install_cmd = (
        f'amx-cli -g "Device.SoftwareModules.InstallDu('
        f'URL=\'{lcm_cfg["package_url"]}\', '
        f'ExecutionEnvRef=\'Device.SoftwareModules.ExecutionUnit.1.\')" '
    )
    
    print(f"Sending Install command: {install_cmd}")
    exec_ssh_command(gateway['ip'], gateway['ssh_user'], gateway['ssh_pass'], install_cmd)

    # 2. Polling kiểm tra trạng thái (vì cài đặt là bất đồng bộ)
    max_retries = 10
    installed = False
    
    for i in range(max_retries):
        time.sleep(5) # Đợi 5s mỗi lần check
        
        # Kiểm tra trạng thái trong DeploymentUnit
        check_cmd = f'amx-cli -g "Device.SoftwareModules.DeploymentUnit.*.Status"'
        status_output = exec_ssh_command(gateway['ip'], gateway['ssh_user'], gateway['ssh_pass'], check_cmd)
        
        if lcm_cfg['package_name'] in status_output and "Installed" in status_output:
            installed = True
            break
        print(f"Retrying... Status currently: {status_output}")

    assert installed is True, f"App {lcm_cfg['package_name']} không đạt trạng thái Installed sau {max_retries*5}s"

def test_lcm_uninstall_via_datamodel(config):
    gateway = config['gateway']
    lcm_cfg = config['lcm']

    # Lệnh Uninstall: Device.SoftwareModules.DeploymentUnit.1.Uninstall()
    # Lưu ý: Cần xác định đúng Index của DU vừa cài
    uninstall_cmd = f'amx-cli -g "Device.SoftwareModules.DeploymentUnit.{lcm_cfg["package_name"]}.Uninstall()"'
    exec_ssh_command(gateway['ip'], gateway['ssh_user'], gateway['ssh_pass'], uninstall_cmd)
    
    # Verify dọn dẹp
    check_cmd = f'amx-cli -g "Device.SoftwareModules.DeploymentUnit.*.Name"'
    output = exec_ssh_command(gateway['ip'], gateway['ssh_user'], gateway['ssh_pass'], check_cmd)
    assert lcm_cfg['package_name'] not in output
