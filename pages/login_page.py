from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ACCESSIBILITY_ID, "username_field")
    PASSWORD = (By.ACCESSIBILITY_ID, "password_field")
    LOGIN_BTN = (By.ACCESSIBILITY_ID, "login_button")
    ERROR = (By.ACCESSIBILITY_ID, "error_message")

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.hide_keyboard()
        self.click(self.LOGIN_BTN)
        return self

    def get_error(self):
        return self.get_text(self.ERROR)
