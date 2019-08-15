Feature: basic stuff

#  Scenario: Load Main Page
#    Given I load Santiment stage page
#    Then page title is "SANbase"

#    Scenario: View Main Page Text
#      Given I load Santiment stage page
#      Then I ensure main page is displayed

#    Scenario: View Main Page Text
#      Given I load Santiment stage page
#      Then I ensure main page is displayed
#      When I search for "Ethereum" in graph search bar

#  Scenario: Select Period
#    Given I load Santiment stage page
#    Then I ensure main page is displayed
#    When I select "1y" period

#  Scenario: Select Category
#    Given I load Santiment stage page
#    Then I ensure main page is displayed
#    When I select "Development" category

# Scenario: Select Metric
#    Given I load Santiment stage page
#    Then I ensure main page is displayed
#    When I search for "Ethereum" in graph search bar
#    When I select "Twitter" metric
#    and I deselect "Price" metric

#   Scenario: Clear all metrics
#    Given I load Santiment stage page
#    When I search for "Ethereum" in graph search bar
#    When I select "1m" period
#    When I select "Twitter" metric
#    and I select "Volume" metric
#    and I select "Development Activity" metric
#    When I clear all active metrics
#    Then I ensure main page is displayed

# Scenario: Select Metric New
#    Given I load Santiment stage page
#    When I clear all active metrics
#    When I select "Price" metric
#    When I select "Volume" metric
#    When I deselect "Price" metric
#    When I clear all active metrics
#    Then I ensure main page is displayed


 Scenario Outline: Verify Link
    Given I load Santiment stage page
    When I search for "<token>" in graph search bar
    When I select "1m" period
    When I select "Development Activity" metric
    When I select "Volume" metric
    Then I verify that share link contains correct data
Examples:
| token |
#| Bitcoin |
#| Litecoin |
#| Cardano |
#| Ripple |
#| ChainLink |
#| Santiment |
#| Stellar |
| Tezos |
| Binance Coin |
#| TRON |
