from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from config.config import APPIUM_SERVER, ANDROID_CAPABILITIES, IOS_CAPABILITIES


class DriverFactory:
    @staticmethod
    def create_driver(platform="android"):
        if platform == "android":
            options = UiAutomator2Options()
            capabilities = ANDROID_CAPABILITIES
        elif platform == "ios":
            options = XCUITestOptions()
            capabilities = IOS_CAPABILITIES
        else:
            raise ValueError(f"Unsupported platform: {platform}")

        for key, value in capabilities.items():
            if value is not None:
                options.set_capability(key, value)

        return webdriver.Remote(APPIUM_SERVER, options=options)
