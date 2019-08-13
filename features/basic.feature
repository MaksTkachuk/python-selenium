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

 Scenario: Select Metric
    Given I load Santiment stage page
    Then I ensure main page is displayed
    When I search for "Ethereum" in graph search bar
    When I select "Twitter" metric
    and I deselect "Price" metric
