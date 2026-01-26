from behave import given, when, then

@given("the cart contains a product")
def step_cart_ready(context):
    context.products_page.add_backpack_to_cart()
    context.products_page.go_to_cart()
    assert context.cart_page.is_product_in_cart()
    context.cart_page.click_checkout()

@when("the user completes the checkout")
def step_complete_checkout(context):
    context.checkout_page.fill_checkout_form("Juan", "Perez", "12345")
    context.checkout_page.finish_checkout()

@then("the order is completed successfully")
def step_order_success(context):
    assert context.checkout_page.get_success_message() == "Thank you for your order!"