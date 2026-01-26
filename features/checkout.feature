Feature: Checkout

    Scenario: Complete purchase successfully
        Given the user is logged in
        And the cart contains a product
        When the user completes the checkout
        Then the order is completed successfully