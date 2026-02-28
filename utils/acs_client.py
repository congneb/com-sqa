import requests
import json

class GenieACSClient:
    def __init__(self, config):
        self.base_url = config['api_url']
        self.device_id = config['device_id']

    def set_parameter(self, path, value):
        # Tạo bản tin đẩy xuống thiết bị qua NBI của GenieACS
        url = f"{self.base_url}/devices/{self.device_id}/tasks"
        payload = {
            "name": "setParameterValues",
            "parameterValues": [[path, value, "xsd:string"]]
        }
        response = requests.post(url, json=payload)
        return response.status_code == 200

    def refresh_object(self, path):
        # Bắt buộc ACS kéo lại dữ liệu mới nhất từ Gateway (GetParameterValues)
        url = f"{self.base_url}/devices/{self.device_id}/tasks"
        payload = {"name": "getParameterValues", "parameterNames": [path]}
        requests.post(url, json=payload)

    """
    hàm để gửi lệnh Reboot (RPC reboot) tới thiết bị qua GenieACS NBI.
    """
    def reboot_device(self):
        # Gửi task Reboot tới device_id xác định
        url = f"{self.base_url}/devices/{self.device_id}/tasks"
        payload = {"name": "reboot"}
        response = requests.post(url, json=payload)
        return response.status_code == 200

    def add_object(self, path):
        # Gửi task addObject tới device_id
        # Ví dụ path: Device.DHCPv4.Server.Pool.1.StaticAddress.
        url = f"{self.base_url}/devices/{self.device_id}/tasks"
        payload = {"name": "addObject", "objectName": path}
        response = requests.post(url, json=payload)
        return response.status_code == 200

    def delete_object(self, object_path):
        # Gửi task deleteObject tới device_id
        # object_path phải bao gồm cả Index, ví dụ: Device.DHCPv4.Server.Pool.1.StaticAddress.1.
        url = f"{self.base_url}/devices/{self.device_id}/tasks"
        payload = {"name": "deleteObject", "objectName": object_path}
        response = requests.post(url, json=payload)
        return response.status_code == 200
