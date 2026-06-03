# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Mobile UI test automation framework using **Appium** + **Pytest**, structured around the
Page Object Model (POM). The same test logic targets both Android (UiAutomator2) and iOS
(XCUITest); the platform is selected at runtime, not by separate code paths.

## Commands

```bash
# Setup
pip install -r requirements.txt

# Run all tests (defaults to Android — see conftest.py pytest_addoption)
pytest

# Choose platform via custom CLI option
pytest --platform=ios
pytest --platform=android

# Filter by marker (markers are declared in pytest.ini)
pytest -m android
pytest -m ios

# Run a single file / class / test
pytest tests/test_login_android.py
pytest tests/test_login_android.py::TestLoginAndroid
pytest tests/test_login_android.py::TestLoginAndroid::test_login_success
```

A running **Appium server at `http://localhost:4723`** and a live emulator/simulator (or
device) are required for tests to execute — there is no mock driver. App binaries are
expected at `apps/android-app.apk` and `apps/ios-app.app` (gitignored).

## Architecture

The flow is: **test → `TestBase` fixture → `DriverFactory` → driver → Page Objects → `BasePage` helpers.**

- **`config/config.py`** — single source of truth for Appium capabilities
  (`ANDROID_CAPABILITIES`, `IOS_CAPABILITIES`), the server URL, and the two timeout
  constants (`IMPLICIT_TIMEOUT`, `EXPLICIT_TIMEOUT`). `BASE_DIR` is used to resolve app
  paths. Every value is **overridable via environment variables** (e.g. `APPIUM_SERVER`,
  `ANDROID_PLATFORM_VERSION`, `IOS_DEVICE_NAME`, `ANDROID_NO_RESET`, `IMPLICIT_TIMEOUT`);
  the hardcoded literals are only defaults via the `_env_str/_env_int/_env_bool` helpers.
  A project-root `.env` is auto-loaded if `python-dotenv` is installed (the import is
  optional — real env vars work without it). See `.env.example` for the full variable list.
  This is what lets the same code run against local emulators and remote device farms
  (BrowserStack/Sauce Labs) without code edits.

- **`utils/driver_factory.py`** — `DriverFactory.create_driver(platform)` maps the platform
  string to the right options class (`UiAutomator2Options` / `XCUITestOptions`), applies the
  capabilities dict, and returns a `webdriver.Remote`. This is the only place that talks to
  the Appium server.

- **`utils/test_base.py`** — `TestBase` is the base class every test class inherits. Its
  `autouse` `setup` fixture reads `--platform`, builds the driver, sets the implicit wait,
  and tears the driver down with `driver.quit()`. It also provides a per-test key/value
  store (`set_data` / `get_data` / `load_data`) used to pass data dicts (from `data/`) into
  the test body. `self.driver`, `self.platform`, `self.test_name`, `self.timestamp` are
  available to subclasses.

- **`tests/conftest.py`** — registers the `--platform` option and wires up
  **automatic screenshot-on-failure**: the `pytest_runtest_makereport` hook stashes each
  phase's report on the item, and the `screenshot_on_failure` autouse fixture saves
  `screenshots/<test_name>_failed.png` when the call phase fails. Screenshots and logs are
  gitignored.

- **`pages/base_page.py`** — `BasePage` wraps all element interaction with explicit
  `WebDriverWait` (via `EXPLICIT_TIMEOUT`) and structured logging. Action methods (`click`,
  `type`, etc.) return `self` to allow chaining. Includes gesture helpers (`swipe_*`,
  `scroll_to`) computed from `driver.get_window_size()`, so they are resolution-independent.

- **`pages/login_page.py`** — example Page Object. Locators are class-level tuples
  (`(By.ACCESSIBILITY_ID, "...")`); methods express user intent (`login`, `get_error`).

- **`data/test_data.py`** — plain dict fixtures (`VALID_USER`, etc.) consumed via
  `TestBase.load_data`.

## Conventions

- **New screens:** add a Page Object in `pages/` subclassing `BasePage`, with locators as
  class-level `(By.X, "value")` tuples and intent-named methods. Prefer `By.ACCESSIBILITY_ID`
  so locators are shared across Android and iOS (the existing pages rely on this for
  cross-platform reuse).
- **New tests:** subclass `TestBase`, apply `@pytest.mark.android` / `@pytest.mark.ios`, and
  use `self.driver`. Do not instantiate drivers manually — the fixture owns the lifecycle.
- **Cross-platform tests:** the Android and iOS login tests are near-identical and differ
  only by marker. Keep shared logic identical so the same Page Objects drive both platforms.
- Use `BasePage` interaction methods rather than calling Appium/Selenium directly, so waits
  and logging stay consistent (note `tests/test_login_*.py` still use
  `driver.find_element` for the final assertion — prefer a Page Object method when extending).
