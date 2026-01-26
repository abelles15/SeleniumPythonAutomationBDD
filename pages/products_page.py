from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductsPage(BasePage):

    # ===== Locators =====
    TITLE = (By.CLASS_NAME, "title")

    ADD_BACKPACK_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")
    REMOVE_BACKPACK_BUTTON = (By.ID, "remove-sauce-labs-backpack")
    ADD_FLEECEJACKET_BUTTON = (By.ID, "add-to-cart-sauce-labs-fleece-jacket")
    ADD_ONESIE_BUTTON = (By.ID, "add-to-cart-sauce-labs-onesie")

    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    # ===== Actions =====
    def is_products_page_displayed(self):
        return self.get_text(self.TITLE) == "Products"

    def add_backpack_to_cart(self):
        self.click(self.ADD_BACKPACK_BUTTON)

    def add_fleecejacket_to_cart(self):
        self.click(self.ADD_FLEECEJACKET_BUTTON)

    def add_onesie_to_cart(self):
        self.click(self.ADD_ONESIE_BUTTON)

    def remove_backpack_from_cart(self):
        self.click(self.REMOVE_BACKPACK_BUTTON)

    def go_to_cart(self):
        self.click(self.CART_ICON)

    def get_cart_items_count(self):
        return self.get_text(self.CART_BADGE)