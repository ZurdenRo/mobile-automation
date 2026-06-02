import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import EXPLICIT_TIMEOUT

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_TIMEOUT)
        logger.debug(f"Initialized {self.__class__.__name__} with timeout={EXPLICIT_TIMEOUT}s")

    def find(self, locator):
        logger.debug(f"Finding element: {locator}")
        element = self.wait.until(EC.presence_of_element_located(locator))
        logger.debug(f"Element found: {locator}")
        return element

    def find_all(self, locator):
        logger.debug(f"Finding all elements: {locator}")
        elements = self.wait.until(EC.presence_of_all_elements_located(locator))
        logger.debug(f"Found {len(elements)} element(s) for: {locator}")
        return elements

    def click(self, locator):
        logger.info(f"Clicking element: {locator}")
        self.find(locator).click()
        logger.debug(f"Clicked successfully: {locator}")
        return self

    def type(self, locator, text):
        logger.info(f"Typing into element: {locator}")
        element = self.find(locator)
        element.clear()
        element.send_keys(text)
        logger.debug(f"Text entered into: {locator}")
        return self

    def get_text(self, locator):
        text = self.find(locator).text
        logger.debug(f"Got text from {locator}: '{text}'")
        return text

    def get_attribute(self, locator, attribute):
        value = self.find(locator).get_attribute(attribute)
        logger.debug(f"Got attribute '{attribute}' from {locator}: '{value}'")
        return value

    def is_visible(self, locator, timeout=None):
        wait_timeout = timeout or EXPLICIT_TIMEOUT
        logger.debug(f"Checking visibility of: {locator} (timeout={wait_timeout}s)")
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            wait.until(EC.visibility_of_element_located(locator))
            logger.debug(f"Element is visible: {locator}")
            return True
        except TimeoutException:
            logger.debug(f"Element is NOT visible: {locator}")
            return False

    def wait_until_visible(self, locator, timeout=None):
        wait_timeout = timeout or EXPLICIT_TIMEOUT
        logger.info(f"Waiting for element to be visible: {locator} (timeout={wait_timeout}s)")
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        return wait.until(EC.visibility_of_element_located(locator))

    def swipe(self, start_x, start_y, end_x, end_y, duration=1000):
        logger.debug(f"Swiping from ({start_x},{start_y}) to ({end_x},{end_y}) duration={duration}ms")
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    def swipe_up(self, duration=1000):
        logger.debug(f"Swiping up (duration={duration}ms)")
        size = self.driver.get_window_size()
        x = size["width"] // 2
        self.swipe(x, int(size["height"] * 0.8), x, int(size["height"] * 0.2), duration)

    def swipe_down(self, duration=1000):
        logger.debug(f"Swiping down (duration={duration}ms)")
        size = self.driver.get_window_size()
        x = size["width"] // 2
        self.swipe(x, int(size["height"] * 0.2), x, int(size["height"] * 0.8), duration)

    def swipe_left(self, duration=1000):
        logger.debug(f"Swiping left (duration={duration}ms)")
        size = self.driver.get_window_size()
        y = size["height"] // 2
        self.swipe(int(size["width"] * 0.8), y, int(size["width"] * 0.2), y, duration)

    def swipe_right(self, duration=1000):
        logger.debug(f"Swiping right (duration={duration}ms)")
        size = self.driver.get_window_size()
        y = size["height"] // 2
        self.swipe(int(size["width"] * 0.2), y, int(size["width"] * 0.8), y, duration)

    def scroll_to(self, locator, max_swipes=5, direction="up"):
        logger.info(f"Scrolling {direction} to find element: {locator} (max_swipes={max_swipes})")
        for i in range(max_swipes):
            if self.is_visible(locator, timeout=2):
                logger.debug(f"Element found after {i} swipe(s): {locator}")
                return self.find(locator)
            if direction == "up":
                self.swipe_up()
            elif direction == "down":
                self.swipe_down()
        logger.error(f"Element not found after {max_swipes} swipes: {locator}")
        raise NoSuchElementException(f"Element not found after scrolling: {locator}")

    def hide_keyboard(self):
        logger.debug("Hiding keyboard")
        self.driver.hide_keyboard()
        logger.debug("Keyboard hidden")

    def take_screenshot(self, name):
        path = f"screenshots/{name}.png"
        self.driver.save_screenshot(path)
        logger.info(f"Screenshot saved: {path}")
        return path

    def back(self):
        logger.info("Pressing back")
        self.driver.back()
