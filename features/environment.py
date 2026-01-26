import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

def before_scenario(context, scenario):
    browser = context.config.userdata.get("browser", "firefox")
    headless = context.config.userdata.get("headless", "false").lower() == "true"

    # DRIVER INIT
    if browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        service = FirefoxService(log_output=os.devnull)
        context.driver = webdriver.Firefox(service=service,options=options)

    elif browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-save-password-bubble")
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        context.driver = webdriver.Chrome(options=options)

    elif browser == "edge":
        options = EdgeOptions()
        options.add_argument("--inprivate")
        if headless:
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")
        context.driver = webdriver.Edge(options=options)

    else:
        raise ValueError(f"Browser not supported: {browser}")

    context.driver.maximize_window()

    # PAGE OBJECTS
    context.login_page = LoginPage(context.driver)
    context.products_page = ProductsPage(context.driver)
    context.cart_page = CartPage(context.driver)
    context.checkout_page = CheckoutPage(context.driver)

def after_scenario(context, scenario):
    if scenario.status == "failed":
        take_screenshot(context, scenario)
    context.driver.quit()

def take_screenshot(context, scenario):
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    scenario_name = scenario.name.replace(" ", "_")
    filename = f"SCENARIO_{scenario_name}_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)
    context.driver.save_screenshot(filepath)
    print(f"\n📸 Screenshot saved: {filepath}")