from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import logging

class Mainpage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.metrics = {
        "Price": "Financial",
        "Volume": "Financial",
        "Development Activity": "Development",
        "Twitter": "Social",
        "Social Volume": "Social",
        "Social Dominance": "Social",
        "Daily Active Deposits": "On-chain",
        "Exchange Flow Balance": "On-chain",
        "Eth Spent Over Time": "On-chain",
        "In Top Holders Total": "On-chain",
        "Percent of Token Supply on Exchanges": "On-chain",
        "Realized Value": "On-chain",
        "Market Value To Realized Value": "On-chain",
        "NVT Ratio Transaction Volume": "On-chain",
        "Network Growth": "On-chain",
        "Daily Active Addresses": "On-chain",
        "Token Age Consumed": "On-chain",
        "Token Velocity": "On-chain",
        "Transaction Volume": "On-chain",
        "Token Circulation": "On-chain"
        }

    def close_cookie_popup(self):
        xpath = "//button[text()='Accept']"
        logging.info("Trying to close cookie popup")
        try:
            button = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            button.click()
        except TimeoutException:
            logging.info("Already closed")
        self.wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))
        logging.info("Closed successfully")

    def get_page_element(self):
        return self.driver.find_element_by_css_selector('div#root div.ChartPage_tool__2vx_W')

    def get_search_wrapper_element(self):
        return self.get_page_element().find_element_by_css_selector('div.SearchWithSuggestions_wrapper__3BM6h')

    def get_search_input_element(self):
        logging.info("Getting search input")
        return self.get_search_wrapper_element().find_element_by_css_selector('input')

    def get_search_result_element(self, text):
        logging.info("Getting search result for '{0}'".format(text))
        search_wrapper_element = self.get_search_wrapper_element()
        search_input_element = self.get_search_input_element()
        search_input_element.send_keys(text)
        xpath = "//button[contains(@class, SearchWithSuggestions_suggestion__AqZNi)]//span[text()='{0}']/././.".format(text)
        search_result_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return search_result_element

    def search(self, text):
        logging.info("Searching for '{0}'".format(text))
        self.get_search_result_element(text).click()
        xpath = "//button[contains(@class, SearchWithSuggestions_suggestion__AqZNi)]//span[text()='{0}']/././.".format(text)
        self.wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))

    def get_period_selector_element(self, period):
        logging.info("Getting period selector for {0}".format(period))
        xpath = "//div[contains(@class, 'ChartPage_ranges__3h7wX')]//div[text()='{0}']".format(period)
        return self.get_page_element().find_element_by_xpath(xpath)

    def select_period(self, period):
        logging.info("Selecting period {0}".format(period))
        xpath = "//div[contains(@class, 'Selector_selected__2rsUx') and text()='{0}']".format(period)
        if len(self.get_page_element().find_elements_by_xpath(xpath)) == 0:
            self.get_period_selector_element(period).click()
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def get_metrics_container_element(self):
        return self.get_page_element().find_element_by_css_selector('div.ChartPage_container__2avm9.ChartPage_container_bottom__3Cwyv')

    def get_metrics_categories_element(self):
        return self.get_metrics_container_element().find_element_by_css_selector('div.ChartMetricSelector_column__2SqCU.ChartMetricSelector_categories__uBPiA')

    def get_metrics_category_element(self, category):
        logging.info("Getting metrics category element {0}".format(category))
        xpath = "//button[contains(text(), '{0}') and contains(@class, 'ChartMetricSelector_btn__1PClN')]".format(category)
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def select_metrics_category(self, category):
        logging.info("Selecting metrics category {0}".format(category))
        xpath = "//button[contains(text(), '{0}') and contains(@class, 'Button_active__3FPKU')]".format(category)
        try:
            logging.info("Checking if metrics category {0} is active".format(category))
            self.get_page_element().find_element_by_xpath(xpath)
            logging.info("Metrics category {0} is active, doing nothing".format(category))
        except NoSuchElementException:
            logging.info("Metrics category {0} is not active, opening it".format(category))
            self.get_metrics_category_element(category).click()
            logging.info("Waiting until metrics category {0} becomes active".format(category))
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def get_metrics_list_element(self):
        selector = 'div.ChartMetricSelector_group__FhAJt'
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def get_metric_element(self, metric):
        logging.info("Getting metric element {0}".format(metric))
        xpath = "//button[contains(text(), '{0}')]".format(metric)
        time.sleep(5)
        return self.get_metrics_list_element().find_element_by_xpath(xpath)

    def get_active_metrics_panel_element(self):
        selector = 'section.ChartActiveMetrics_wrapper__3Z0I8'
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def get_active_metric_element(self, metric):
        logging.info("Getting active metric element {0}".format(metric))
        xpath = "//button[contains(text(), '{0}')]".format(metric)
        return self.get_active_metrics_panel_element().find_element_by_xpath(xpath)

    def select_metric(self, metric):
        logging.info("Selecting metric {0}".format(metric))
        try:
            logging.info("Looking for '{0}' in active metrics".format(metric))
            self.get_active_metric_element(metric)
        except NoSuchElementException:
            logging.info("Havent found '{0}' in active metrics, opening it".format(metric))
            self.select_metrics_category(self.metrics[metric])
            self.get_metric_element(metric).click()
            self.wait.until(EC.visibility_of(self.get_active_metric_element(metric)))

    def deselect_metric(self, metric):
        logging.info("Deselecting metric {0}".format(metric))
        try:
            logging.info("Looking for '{0}' in active metrics".format(metric))
            active_metric = self.get_active_metric_element(metric)
            logging.info("Found '{0}' in active metrics, closing it".format(metric))
            active_metric.click()
            self.wait.until(EC.invisibility_of_element(self.get_active_metric_element(metric)))
        except NoSuchElementException:
            logging.info("Havent found '{0}' in active metrics".format(metric))

    def clear_all_active_metrics(self):
        for button in self.get_active_metrics_panel_element().find_elements_by_xpath("//button"):
            button.click()
            self.wait.until(EC.invisibility_of_element(button))

    def get_share_button(self):
        return self.get_page_element().find_element_by_css_selector('button.ShareBtn_btn__aWeOd')

    def get_share_dialog(self):
        selector = 'div.Dialog_modal__1QXQD.Panel_panel__280Ap'
        return self.driver.find_element_by_css_selector(selector)

    def get_share_link_element(self):
        selector = 'input.Input_input__1XjEb.SharePanel_link__input__2bRzG'
        return self.get_share_dialog().find_element_by_css_selector(selector)

    def get_share_link_value(self):
        return self.get_share_link_element().get_attribute('value')

    def open_share_dialog(self):
        logging.info("Opening share dialog")
        try:
            logging.info("Checking if share dialog is open")
            self.get_share_dialog()
            logging.info("Share dialog is open, doing nothing")
        except NoSuchElementException:
            logging.info("Share dialog is not open, clicking the button")
            self.get_share_button().click()
            logging.info("Waiting until share dialog is open")
            self.wait.until(EC.visibility_of(self.get_share_dialog()))


    def close_share_dialog(self):
        try:
            dialog = self.get_share_dialog()
            close_button = dialog.find_element_by_css_selector('svg.Dialog_close__wPN0y')
            close_button.click()
            self.wait.until(EC.invisibility_of_element(self.get_share_dialog()))
        except NoSuchElementException:
            pass
