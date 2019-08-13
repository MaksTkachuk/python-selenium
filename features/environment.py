from behave import fixture, use_fixture
from selenium import webdriver
import sys, os

chromedriver_path = os.path.realpath(os.path.join(os.getcwd(), '..', 'bin', 'chromedriver'))

@fixture
def selenium_browser_chrome(context):
    if chromedriver_path not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + chromedriver_path
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    context.browser = webdriver.Chrome(chrome_options=options)
    yield context.browser
    context.browser.quit()

def before_all(context):
    use_fixture(selenium_browser_chrome, context)
