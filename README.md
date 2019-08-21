# python-selenium
This project contains some e2e automated tests for Santiment's stage server (https://app-stage.santiment.net)

Tests are based on Page Object Model (POM), and cover the following functionality:

-searching a token

-choosing a time period

-selecting/deselecting metrics

-opening/closing the "Share" dialog window


It uses Behave testing framework, tests can be run locally or using Browserstack (https://www.browserstack.com/automate/behave)

Here's a brief summary of the codebase:

datastorage.py - contains constant values which are needed for the tests

main_page.py - contains the POM for the stage server main page

steps.py - contains test steps (more on that here https://behave.readthedocs.io/en/latest/tutorial.html#python-step-implementations)

basic.feature - feature file that contains some basic e2e tests

environment.py - contains setup for Behave and Browserstack integration

To run the tests, in the /features directory run:

behave
