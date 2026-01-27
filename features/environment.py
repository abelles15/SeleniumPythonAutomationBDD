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
import allure

def before_scenario(context, scenario):
    browser = context.config.userdata.get("browser", "firefox")
    headless = context.config.userdata.get("headless", "false").lower() == "false" #The browser is not opened during executions

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

    context.driver.set_window_size(1920, 1080)
    context.driver.execute_script("document.body.style.zoom='100%'")

    # PAGE OBJECTS
    context.login_page = LoginPage(context.driver)
    context.products_page = ProductsPage(context.driver)
    context.cart_page = CartPage(context.driver)
    context.checkout_page = CheckoutPage(context.driver)

def take_screenshot(context, scenario):
    screenshots_dir = "reports/allure-results"
    os.makedirs(screenshots_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    scenario_name = scenario.name.replace(" ", "_")
    filename = f"FAILED_{scenario_name}_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)
    context.driver.save_screenshot(filepath)

    allure.attach.file(filepath, name=f"Screenshot - {scenario.name}", attachment_type=allure.attachment_type.PNG)
    print(f"\n📸 Screenshot attached to Allure: {filepath}")

def after_scenario(context, scenario):
    if scenario.status == "failed":
        take_screenshot(context, scenario)
    context.driver.quit()