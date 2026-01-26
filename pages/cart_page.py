from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):

    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def is_product_in_cart(self):
        return self.wait_for_visibility(self.CART_ITEM).is_displayed()

    def click_checkout(self):
        self.click(self.CHECKOUT_BUTTON)