from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
import logging
from typing import NamedTuple
from datetime import datetime
from datastorage import *

class ActiveMetricData(NamedTuple):
    name: str
    active: bool

class MaxAttemptsLimitException(Exception):
    pass

class MissingCategoryException(Exception):
    pass

class MissingMetricException(Exception):
    pass

class ClickError(Exception):
    pass

def safe_click(element):
    attempts = 0
    while attempts < 5:
        try:
            element.click()
            return
        except StaleElementReferenceException:
            attempts += 1
    raise ClickError("Exceeded max click attempts limit on element {0}".format(element))

class Mainpage:

    def __init__(self, driver):
        self.default_url = 'https://app-stage.santiment.net/?from=2019-02-13T21%3A00%3A00.000Z&interval=1d&metrics=historyPrice&slug=bitcoin&title=Bitcoin%20%28BTC%29&to=2019-08-14T21%3A00%3A00.000Z'
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)
        self.state = {
        "active_metrics": [ActiveMetricData('Price', True)],
        }

    def navigate_to_main_page(self):
        attempts = 0
        xpath = xpaths["metrics_category"].format("Financial")
        while attempts < 5:
            try:
                self.driver.get(self.default_url)
                self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                return
            except TimeoutException:
                attempts += 1
        raise MaxAttemptsLimitException("Exceeded max attempts limit trying to load main page")

    def close_cookie_popup(self):
        xpath = xpaths["close_cookies_button"]
        logging.info("Trying to close cookie popup")
        try:
            button = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            safe_click(button)
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            logging.info("Already closed")
        logging.info("Closed successfully")

    def close_explore_popup(self):
        xpath = xpaths["close_assets_button"]
        logging.info("Trying to close explore assets popup")
        try:
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            safe_click(button)
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            logging.info("Already closed")
        logging.info("Closed successfully")

    def get_page_element(self):
        xpath = xpaths["page_element"]
        return self.driver.find_element_by_xpath(xpath)

    def get_search_wrapper_element(self):
        selector = selectors["search_wrapper"]
        return self.get_page_element().find_element_by_css_selector(selector)

    def get_search_input_element(self):
        selector = selectors["search_input"]
        return self.get_search_wrapper_element().find_element_by_css_selector(selector)

    def get_search_result_element(self, text):
        logging.info("Getting search result for '{0}'".format(text))
        xpath = xpaths["search_result"]
        search_result_elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        for element in search_result_elements:
            if text.lower() in element.text.lower():
                    return element

    def search(self, text):
        logging.info("Searching for '{0}'".format(text))
        search_input_element = self.get_search_input_element()
        search_input_element.send_keys(text)
        safe_click(self.get_search_result_element(text))
        xpath = xpaths["search_result"].format(text)
        self.wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))

    def get_period_selector_element(self, period):
        logging.info("Getting period selector for {0}".format(period))
        xpath = xpaths["period_selector"].format(period)
        return self.get_page_element().find_element_by_xpath(xpath)

    def select_period(self, period):
        logging.info("Selecting period {0}".format(period))
        xpath = xpaths["period_selector_active"].format(period)
        safe_click(self.get_period_selector_element(period))
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def get_metrics_container_element(self):
        selector = selectors["metrics_container"]
        return self.get_page_element().find_element_by_css_selector(selector)

    def get_metrics_categories_element(self):
        selector = selectors["metrics_categories"]
        return self.get_metrics_container_element().find_element_by_css_selector(selector)

    def get_metrics_category_element(self, category):
        logging.info("Getting metrics category element {0}".format(category))
        xpath = xpaths["metrics_category"].format(category)
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def select_metrics_category(self, category):
        logging.info("Selecting metrics category {0}".format(category))
        xpath_active = xpaths["metrics_category"].format(category)
        try:
            safe_click(self.get_metrics_category_element(category))
        except TimeoutException:
            raise MissingCategoryException("Category {0} not found for the selected token".format(category))
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath_active)))


    def get_metrics_list_element(self):
        selector = selectors["metrics_list"]
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def get_metric_element(self, metric):
        logging.info("Getting metric element {0}".format(metric))
        xpath = xpaths["metric"].format(metric)
        try:
            return self.get_metrics_list_element().find_element_by_xpath(xpath)
        except NoSuchElementException:
            raise MissingMetricException("Metric {0} not found for the selected token".format(metric))

    def get_active_metrics_panel_element(self):
        selector = selectors["active_metrics_panel"]
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def get_active_metric_element(self, metric):
        logging.info("Getting active metric element {0}".format(metric))
        xpath = xpaths["active_metric"].format(metric)
        return self.get_active_metrics_panel_element().find_element_by_xpath(xpath)

    def select_metric(self, metric):
        if not metric in [x.name for x in self.state['active_metrics']]:
            xpath = xpaths["active_metric"].format(metric)
            try:
                self.select_metrics_category(metrics[metric][0])
            except MissingCategoryException:
                logging.info("No such category for the selected token")
                return
            try:
                metric_element = self.get_metric_element(metric)
                safe_click(metric_element)
            except MissingMetricException:
                logging.info("No such metric for the selected token")
                return
            try:
                self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                self.state['active_metrics'].append(ActiveMetricData(metric, True))
            except TimeoutException:
                xpath = xpaths["inactive_metric"]
                metric_element.find_element_by_xpath(xpath)
                self.state['active_metrics'].append(ActiveMetricData(metric, False))


    def deselect_metric(self, metric):
        logging.info("Trying to deselect {0} metric".format(metric))
        if ActiveMetricData(metric, True) in self.state['active_metrics']:
            active_metric = self.get_active_metric_element(metric)
            safe_click(active_metric)
            self.wait.until(EC.invisibility_of_element(active_metric))
            self.state['active_metrics'].remove(ActiveMetricData(metric, True))

    def clear_all_active_metrics(self):
        logging.info("{0} active metrics to remove".format(len(self.state['active_metrics'])))
        for metric in self.state['active_metrics']:
            self.deselect_metric(metric.name)
        logging.info("{0} metrics left after removal".format(len(self.state['active_metrics'])))

    def get_share_button(self):
        return self.get_page_element().find_element_by_css_selector('button.ShareBtn_btn__aWeOd')

    def get_share_dialog(self):
        selector = selectors["share_dialog"]
        return self.driver.find_element_by_css_selector(selector)

    def get_share_link_element(self):
        selector = selectors["share_link"]
        return self.get_share_dialog().find_element_by_css_selector(selector)

    def get_share_link_value(self):
        return self.get_share_link_element().get_attribute('value')

    def open_share_dialog(self):
        logging.info("Opening share dialog")
        selector = selectors["share_dialog"]
        try:
            logging.info("Checking if share dialog is open")
            self.get_share_dialog()
            logging.info("Share dialog is open, doing nothing")
        except NoSuchElementException:
            logging.info("Share dialog is not open, clicking the button")
            safe_click(self.get_share_button())
            logging.info("Waiting until share dialog is open")
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))


    def close_share_dialog(self):
        selector = selectors["close_share_dialog"]
        try:
            dialog = self.get_share_dialog()
            close_button = dialog.find_element_by_css_selector(selector)
            safe_click(close_button)
            self.wait.until(EC.invisibility_of_element(dialog))
        except NoSuchElementException:
            pass

    def get_graph_title(self):
        selector = selectors["graph_title"]
        return self.get_page_element().find_element_by_css_selector(selector).text

    def get_from_to_dates(self):
        selector = selectors["calendar_dates"]
        [date_from_text, date_to_text] = self.get_page_element().find_element_by_css_selector(selector).text.split('-')
        datetime_from = datetime.strptime(date_from_text.strip(), '%d.%m.%y')
        datetime_to = datetime.strptime(date_to_text.strip(), '%d.%m.%y')
        return datetime_from, datetime_to

    def get_interval(self):
        selector = selectors["interval"]
        return self.get_page_element().find_element_by_css_selector(selector).text
