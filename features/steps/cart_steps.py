from behave import then

@then("the product is displayed in the cart")
def step_product_in_cart(context):
    assert context.cart_page.is_product_in_cart()