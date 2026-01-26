from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class ProductsPage(BasePage):

    ADD_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    ADD_FLEECE = (By.ID, "add-to-cart-sauce-labs-fleece-jacket")
    ADD_ONESIE = (By.ID, "add-to-cart-sauce-labs-onesie")

    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

    PRODUCTS_TITLE = (By.CLASS_NAME, "title")

    def is_products_page_displayed(self) -> bool:
        try:
            return self.wait.until(EC.visibility_of_element_located(self.PRODUCTS_TITLE)).text == "Products"
        except Exception:
            return False

    def add_backpack_to_cart(self):
        self._add_product(self.ADD_BACKPACK)

    def add_fleecejacket_to_cart(self):
        self._add_product(self.ADD_FLEECE)

    def add_onesie_to_cart(self):
        self._add_product(self.ADD_ONESIE)

    def _add_product(self, add_locator, timeout=5):
        add_btn = self.wait.until(EC.element_to_be_clickable(add_locator))
        add_btn.click()

        # Wait until add button disappears (product added)
        WebDriverWait(self.driver, timeout).until(EC.staleness_of(add_btn))

    def get_cart_items_count(self):
        return self.wait.until(EC.visibility_of_element_located(self.CART_BADGE)).text

    def go_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.CART_ICON)).click()