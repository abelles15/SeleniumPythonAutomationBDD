from behave import given, when, then

@given("the user is on the login page")
def step_open_login(context):
    context.login_page.open_login_page()

@when('the user logs in with "{username}" and "{password}"')
def step_login(context, username, password):
    context.login_page.login(username, password)

@then("the products page is displayed")
def step_products_page(context):
    assert context.products_page.is_products_page_displayed()

@then('an error message "{message}" is shown')
def step_error_message(context, message):
    assert message in context.login_page.get_error_message()