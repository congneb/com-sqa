from utils.ssh_client import get_tr181_value

def test_change_ssid_with_yaml(page, login_page, gateway_cfg, tr181_paths):
    NEW_SSID = "PrplOS_Yaml_Test"

    # Sử dụng dữ liệu từ config.yaml qua fixture
    login_page.page.goto(gateway_cfg['base_url'])
    login_page.login(gateway_cfg['web_user'], gateway_cfg['web_pass'])
    
    # ... các bước thực hiện thay đổi SSID ...
    wifi_page = WifiPage(page)
    page.goto(f"http://{GATEWAY_IP}/wifi-settings") # URL thực tế của router
    wifi_page.change_ssid(NEW_SSID)
    
    # Đợi hệ thống apply (tùy gateway, có thể cần 5-10s)
    page.wait_for_timeout(5000)


    # Kiểm tra TR-181 bằng SSH
    actual_val = get_tr181_value(
        host=gateway_cfg['ip'],
        user=gateway_cfg['ssh_user'],
        password=gateway_cfg['ssh_pass'],
        path=tr181_paths['ssid_2g']
    )
    assert NEW_SSID in actual_val
