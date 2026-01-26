from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ===== Navigation =====
    def open(self, url):
        self.driver.get(url)

    # ===== Wait helpers =====
    def wait_for_presence(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator), message=f"Element not present: {locator}")

    def wait_for_visibility(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator), message=f"Element not visible: {locator}")

    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator), message=f"Element not clickable: {locator}")

    # ===== Generic actions =====
    def click(self, locator):
        try:
            self.wait_for_clickable(locator).click()
        except TimeoutException as e:
            raise TimeoutException(f"Click failed on {locator}") from e

    def type(self, locator, text, clear=True):
        try:
            element = self.wait_for_visibility(locator)
            if clear:
                element.clear()
            element.send_keys(text)
        except TimeoutException as e:
            raise TimeoutException(f"Typing failed on {locator}") from e

    def get_text(self, locator):
        try:
            return self.wait_for_visibility(locator).text
        except TimeoutException as e:
            raise TimeoutException(f"Get text failed on {locator}") from e