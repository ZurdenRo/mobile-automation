import pytest
from selenium.webdriver.common.by import By
from utils.test_base import TestBase
from pages.login_page import LoginPage
from data.test_data import VALID_USER, INVALID_USER


HOME_TITLE = (By.ACCESSIBILITY_ID, "home_title")


@pytest.mark.ios
class TestLoginIOS(TestBase):
    def test_login_success(self):
        self.load_data(VALID_USER)
        LoginPage(self.driver).login(
            self.get_data("username"),
            self.get_data("password"),
        )
        assert self.driver.find_element(*HOME_TITLE).is_displayed()

    def test_login_invalid_credentials(self):
        LoginPage(self.driver).login(
            INVALID_USER["username"],
            INVALID_USER["password"],
        )
        assert "Invalid" in LoginPage(self.driver).get_error()
