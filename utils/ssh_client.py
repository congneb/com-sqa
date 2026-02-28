import paramiko

def get_tr181_value(host, user, password, path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=password)
    
    # Lệnh truy vấn TR-181 SSID trong PrplOS (sử dụng amx-cli hoặc ubus)
    # Ví dụ: Device.WiFi.SSID.1.SSID
    cmd = f'ubus call pcb.Status get \'{{"object": "{path}"}}\''
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read().decode()
    ssh.close()
    return result

def check_system_logs(host, user, password, keyword, lines=50):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=password)
    
    # Đọc n dòng cuối của log hệ thống
    cmd = f"logread | tail -n {lines}"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    log_content = stdout.read().decode()
    ssh.close()
    
    return keyword in log_content, log_content
