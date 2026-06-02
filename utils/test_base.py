import pytest
from datetime import datetime
from utils.driver_factory import DriverFactory
from config.config import IMPLICIT_TIMEOUT


class TestBase:
    @pytest.fixture(autouse=True)
    def setup(self, request):
        self.platform = request.config.getoption("--platform")
        self.driver = DriverFactory.create_driver(self.platform)
        self.driver.implicitly_wait(IMPLICIT_TIMEOUT)
        self.test_name = request.node.name
        self.test_data = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        yield
        if self.driver:
            self.driver.quit()

    def set_data(self, key, value):
        self.test_data[key] = value

    def get_data(self, key, default=None):
        return self.test_data.get(key, default)

    def load_data(self, data):
        if isinstance(data, dict):
            self.test_data.update(data)
