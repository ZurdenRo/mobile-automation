from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

APPIUM_SERVER = "http://localhost:4723"

ANDROID_CAPABILITIES = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "Android Emulator",
    "platformVersion": "13.0",
    "app": str(BASE_DIR / "apps" / "android-app.apk"),
    "appPackage": "com.example.app",
    "appActivity": ".MainActivity",
    "autoGrantPermissions": True,
    "noReset": False,
}

IOS_CAPABILITIES = {
    "platformName": "iOS",
    "automationName": "XCUITest",
    "deviceName": "iPhone 14",
    "platformVersion": "16.0",
    "app": str(BASE_DIR / "apps" / "ios-app.app"),
    "bundleId": "com.example.app",
    "noReset": False,
}

IMPLICIT_TIMEOUT = 10
EXPLICIT_TIMEOUT = 20
