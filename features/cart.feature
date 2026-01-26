Feature: Cart

    Scenario: Add product to cart
        Given the user is logged in
        When the user adds a backpack to the cart
        Then the product is displayed in the cart

    Scenario: Add three products to the shopping cart
        Given the user is logged in
        When the user adds three different products to the cart
        Then the cart badge should show "3" items
