"""Central configuration for the framework.

Every value below can be overridden via environment variables so the same code
runs unchanged across local emulators, teammates' machines, and device farms
(BrowserStack, Sauce Labs, ...). The hardcoded values are only the *defaults*.

Variables are read from the process environment and, if present, from a `.env`
file at the project root (gitignored). See `.env.example` for the full list.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load a project-root .env if python-dotenv is available. The dependency is
# optional: without it, real environment variables still work.
try:
    from dotenv import load_dotenv

    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

def _env_str(key, default):
    value = os.getenv(key)
    return value if value is not None and value != "" else default


def _env_int(key, default):
    value = os.getenv(key)
    if value is None or value == "":
        return default
    return int(value)


def _env_bool(key, default):
    value = os.getenv(key)
    if value is None or value == "":
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


APPIUM_SERVER = _env_str("APPIUM_SERVER", "http://localhost:4723")

ANDROID_CAPABILITIES = {
    "platformName": "Android",
    "automationName": _env_str("ANDROID_AUTOMATION_NAME", "UiAutomator2"),
    "deviceName": _env_str("ANDROID_DEVICE_NAME", "Android Emulator"),
    "platformVersion": _env_str("ANDROID_PLATFORM_VERSION", "13.0"),
    "app": _env_str("ANDROID_APP", str(BASE_DIR / "apps" / "android-app.apk")),
    "appPackage": _env_str("ANDROID_APP_PACKAGE", "com.example.app"),
    "appActivity": _env_str("ANDROID_APP_ACTIVITY", ".MainActivity"),
    "autoGrantPermissions": _env_bool("ANDROID_AUTO_GRANT_PERMISSIONS", True),
    "noReset": _env_bool("ANDROID_NO_RESET", False),
}

IOS_CAPABILITIES = {
    "platformName": "iOS",
    "automationName": _env_str("IOS_AUTOMATION_NAME", "XCUITest"),
    "deviceName": _env_str("IOS_DEVICE_NAME", "iPhone 14"),
    "platformVersion": _env_str("IOS_PLATFORM_VERSION", "16.0"),
    "app": _env_str("IOS_APP", str(BASE_DIR / "apps" / "ios-app.app")),
    "bundleId": _env_str("IOS_BUNDLE_ID", "com.example.app"),
    "noReset": _env_bool("IOS_NO_RESET", False),
}

IMPLICIT_TIMEOUT = _env_int("IMPLICIT_TIMEOUT", 10)
EXPLICIT_TIMEOUT = _env_int("EXPLICIT_TIMEOUT", 20)
