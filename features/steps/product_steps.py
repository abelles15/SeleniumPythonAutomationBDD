from behave import given, when, then

@given("the user is logged in")
def step_user_logged_in(context):
    context.login_page.open_login_page()
    context.login_page.login("standard_user", "secret_sauce")
    assert context.products_page.is_products_page_displayed()

@when("the user adds a backpack to the cart")
def step_add_product(context):
    context.products_page.add_backpack_to_cart()
    context.products_page.go_to_cart()

@when("the user adds three different products to the cart")
def step_add_three_products(context):
    context.products_page.add_backpack_to_cart()
    context.products_page.add_fleecejacket_to_cart()
    context.products_page.add_onesie_to_cart()

@then('the cart badge should show "{count}" items')
def step_cart_badge(context, count):
    assert context.products_page.get_cart_items_count() == count