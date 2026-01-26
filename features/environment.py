import os
from datetime import datetime
from selenium import webdriver

from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

def before_scenario(context, scenario):
    browser = context.config.userdata.get("browser", "firefox")

    if browser == "chrome":
        context.driver = webdriver.Chrome()
    elif browser == "firefox":
        context.driver = webdriver.Firefox()
    elif browser == "edge":
        context.driver = webdriver.Edge()
    else:
        raise ValueError(f"Browser not supported: {browser}")

    context.driver.maximize_window()

    # Init Pages
    context.login_page = LoginPage(context.driver)
    context.products_page = ProductsPage(context.driver)
    context.cart_page = CartPage(context.driver)
    context.checkout_page = CheckoutPage(context.driver)

def after_scenario(context, scenario):
    # 📸 Screenshot only when fails
    if scenario.status == "failed":
        take_screenshot(context, scenario)

    context.driver.quit()

def take_screenshot(context, scenario):
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    scenario_name = scenario.name.replace(" ", "_")
    filename = f"{scenario_name}_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)
    context.driver.save_screenshot(filepath)
    print(f"\n📸 Screenshot guardado en: {filepath}")