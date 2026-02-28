import yaml
import os

def load_config():
    # Xác định đường dẫn tuyệt đối đến file config.yaml
    base_path = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(base_path, "config.yaml")
    
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

# Khởi tạo một object config dùng chung
config = load_config()
