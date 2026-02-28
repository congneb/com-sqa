import pytest
from utils.config_loader import config

@pytest.fixture(scope="session")
def gateway_cfg():
    return config['gateway']

@pytest.fixture(scope="session")
def tr181_paths():
    return config['tr181_paths']
