from behave import *
from main_page import Mainpage

@Given('I load Santiment stage page')
def step_impl(context):
    context.browser.get("https://app-stage.santiment.net")
    context.mainpage = Mainpage(context.browser)
    context.mainpage.close_cookie_popup()

@Then('page title is "{title}"')
def step_impl(context, title):
    assert context.browser.title == title

@Then('I ensure main page is displayed')
def step_impl(context):
    assert context.mainpage.get_page_element().is_displayed() == True

@When('I search for "{text}" in graph search bar')
def step_impl(context, text):
    context.mainpage.search(text)

@When('I select "{period}" period')
def step_impl(context, period):
    context.mainpage.select_period(period)

@When('I select "{category}" category')
def step_impl(context, category):
    context.mainpage.select_metrics_category(category)

@When('I select "{metric}" metric')
def step_impl(context, metric):
    context.mainpage.select_metric(metric)

@When('I deselect "{metric}" metric')
def step_impl(context, metric):
    context.mainpage.deselect_metric(metric)

@When('I open share dialog')
def step_impl(context):
    context.mainpage.open_share_dialog()

@When('I close share dialog')
def step_impl(context):
    context.mainpage.close_share_dialog()

@When('I print share link')
def step_impl(context):
    print(context.mainpage.get_share_link_value())
