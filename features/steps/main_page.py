from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
import logging
from typing import NamedTuple
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datastorage import *

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
        date_to = datetime.strftime(datetime.today(), '%Y-%m-%dT21:00:00.000Z')
        date_from = datetime.strftime(datetime.today() - relativedelta(months=6), '%Y-%m-%dT21:00:00.000Z')
        self.default_url = 'https://app-stage.santiment.net/?from={0}&interval=1d&metrics=historyPrice&slug=bitcoin&title=Bitcoin%20%28BTC%29&to={1}'.format(date_from, date_to)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)
        self.state = {
        "active_metrics": ['Price'],
        }

    def navigate_to_main_page(self):
        attempts = 0
        selector = selectors["token_selector_image"]
        while attempts < 5:
            try:
                self.driver.get(self.default_url)
                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
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

    def get_chart_page_element(self):
        xpath = xpaths["chart_page_element"]
        return self.driver.find_element_by_xpath(xpath)

    def get_search_dialog(self):
        selector = selectors["search_dialog"]
        return self.driver.find_element_by_css_selector(selector)

    def get_search_input_element(self):
        selector = selectors["search_input"]
        return self.get_search_dialog().find_element_by_css_selector(selector)

    def get_search_result_element(self, text):
        logging.info("Getting search result for '{0}'".format(text))
        xpath = xpaths["search_result"]
        search_result_elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        for element in search_result_elements:
            if text.lower() in element.text.lower():
                    return element

    def search(self, text):
        logging.info("Searching for '{0}'".format(text))
        self.open_search_dialog()
        search_input_element = self.get_search_input_element()
        search_input_element.send_keys(text)

    def search_and_select(self, text):
        self.search(text)
        safe_click(self.get_search_result_element(text))
        xpath = xpaths["search_result"].format(text)
        self.wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))

    def get_period_selector_element(self, period):
        logging.info("Getting period selector for {0}".format(period))
        xpath = xpaths["period_selector"].format(period)
        return self.get_chart_page_element().find_element_by_xpath(xpath)

    def select_period(self, period):
        logging.info("Selecting period {0}".format(period))
        xpath = xpaths["period_selector_active"].format(period)
        safe_click(self.get_period_selector_element(period))
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def get_metrics_menu_element(self):
        selector = selectors["metrics_menu"]
        return self.get_chart_page_element().find_element_by_css_selector(selector)

    def get_metrics_categories_element(self):
        selector = selectors["metrics_categories"]
        return self.get_metrics_menu_element().find_element_by_css_selector(selector)

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

    def get_close_active_metric_element(self, active_metric):
        selector = selectors["close_active_metric"]
        return active_metric.find_element_by_css_selector(selector)

    def select_metric(self, metric):
        if not metric in self.state['active_metrics']:
            self.open_metrics_menu()
            xpath = xpaths["active_metric"].format(metric)
            try:
                self.select_metrics_category(metrics[metric][0])
            except MissingCategoryException:
                logging.info("No such category for the selected token")
                self.close_metrics_menu()
                return
            try:
                metric_element = self.get_metric_element(metric)
                safe_click(metric_element)
            except MissingMetricException:
                logging.info("No such metric for the selected token")
                self.close_metrics_menu()
                return
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            self.state['active_metrics'].append(metric)
            self.close_metrics_menu()


    def deselect_metric(self, metric):
        logging.info("Trying to deselect {0} metric".format(metric))
        if metric in self.state['active_metrics']:
            active_metric = self.get_active_metric_element(metric)
            safe_click(self.get_close_active_metric_element(active_metric))
            self.wait.until(EC.invisibility_of_element(active_metric))
            self.state['active_metrics'].remove(metric)

    def clear_all_active_metrics(self):
        logging.info("{0} active metrics to remove".format(len(self.state['active_metrics'])))
        for metric in self.state['active_metrics']:
            self.deselect_metric(metric)
        logging.info("{0} metrics left after removal".format(len(self.state['active_metrics'])))

    def get_share_button(self):
        return self.get_chart_page_element().find_element_by_css_selector('button.ShareBtn_btn__aWeOd')

    def get_share_dialog(self):
        selector = selectors["share_dialog"]
        return self.driver.find_element_by_css_selector(selector)

    def get_share_link_element(self):
        selector = selectors["share_link"]
        return self.get_share_dialog().find_element_by_css_selector(selector)

    def get_share_link_value(self):
        return self.get_share_link_element().get_attribute('value')

    def get_chart_header_element(self):
        selector = selectors["chart_header_element"]
        return self.driver.find_element_by_css_selector(selector)

    def get_token_selector_element(self):
        selector = selectors["token_selector_element"]
        return self.driver.find_element_by_css_selector(selector)

    def open_share_dialog(self):
        logging.info("Opening share dialog")
        selector = selectors["share_dialog"]
        try:
            logging.info("Checking if share dialog is open")
            self.get_share_dialog()
            logging.info("Share dialog is open, doing nothing")
        except NoSuchElementException:
            logging.info("Share dialog is not open, clicking the button")
            self.open_chart_settings_menu()
            safe_click(self.get_chart_settings_menu_item("share"))
            logging.info("Waiting until share dialog is open")
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def close_share_dialog(self):
        selector = selectors["close_share_dialog"]
        logging.info("Closing share dialog")
        try:
            dialog = self.get_share_dialog()
            close_button = dialog.find_element_by_css_selector(selector)
            safe_click(close_button)
            self.wait.until(EC.invisibility_of_element(dialog))
            logging.info("Closed share dialog")
            self.close_chart_settings_menu()
        except NoSuchElementException:
            logging.info("Already closed")
            self.close_chart_settings_menu()

    def open_search_dialog(self):
        selector = selectors["search_dialog"]
        try:
            logging.info("Checking if search dialog is open")
            self.get_share_dialog()
            logging.info("Search dialog is open, doing nothing")
        except NoSuchElementException:
            logging.info("Search dialog is not open, clicking the button")
            safe_click(self.get_token_selector_element())
            logging.info("Waiting until search dialog is open")
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def close_search_dialog(self):
        selector = selectors["close_search_dialog"]
        try:
            dialog = self.get_search_dialog()
            close_button = dialog.find_element_by_css_selector(selector)
            safe_click(close_button)
            self.wait.until(EC.invisibility_of_element(dialog))
        except NoSuchElementException:
            pass

    def get_metrics_menu_element(self):
        selector = selectors["metrics_menu"]
        return self.get_chart_page_element().find_element_by_css_selector(selector)

    def get_metrics_menu_button(self):
        selector = selectors["metrics_menu_button"]
        return self.get_chart_page_element().find_element_by_css_selector(selector)

    def get_modal_overlay(self):
        selector = selectors["modal_overlay"]
        return self.driver.find_element_by_css_selector(selector)

    def open_metrics_menu(self):
        logging.info("Opening metrics menu")
        selector = selectors["metrics_menu"]
        try:
            self.get_metrics_menu_element()
            logging.info("Already opened")
        except NoSuchElementException:
            safe_click(self.get_metrics_menu_button())
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            logging.info("Menu opened")

    def close_metrics_menu(self):
        logging.info("Closing metrics menu")
        selector = selectors["metrics_menu"]
        try:
            safe_click(self.get_modal_overlay())
            self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))
            logging.info("Menu closed")
        except NoSuchElementException:
            logging.info("Already closed")

    def get_chart_settings_button(self):
        selector = selectors["chart_settings_button"]
        return self.get_chart_page_element().find_element_by_css_selector(selector)

    def get_chart_settings_menu_element(self):
        selector = selectors["chart_settings_menu"]
        return self.driver.find_element_by_css_selector(selector)

    def open_chart_settings_menu(self):
        logging.info("Opening chart settings menu")
        selector = selectors["chart_settings_menu"]
        try:
            self.get_chart_settings_menu_element()
            logging.info("Already opened")
        except NoSuchElementException:
            safe_click(self.get_chart_settings_button())
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            logging.info("Menu opened")

    def close_chart_settings_menu(self):
        logging.info("Closing chart settings menu")
        selector = selectors["chart_settings_menu"]
        try:
            safe_click(self.get_modal_overlay())
            self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))
            logging.info("Menu closed")
        except NoSuchElementException:
            logging.info("Already closed")

    def get_chart_settings_menu_item(self, option):
        xpath = xpaths["chart_settings_menu_item"].format(chart_settings_options[option])
        return self.get_chart_settings_menu_element().find_element_by_xpath(xpath)

    def get_token_title(self):
        selector = selectors["token_title"]
        return self.get_token_selector_element().find_element_by_css_selector(selector).text

    def get_from_to_dates(self):
        selector = selectors["calendar_dates"]
        [date_from_text, date_to_text] = self.get_chart_page_element().find_element_by_css_selector(selector).text.split('-')
        datetime_from = datetime.strptime(date_from_text.strip(), '%d.%m.%y')
        datetime_to = datetime.strptime(date_to_text.strip(), '%d.%m.%y')
        return datetime_from, datetime_to

    def get_interval(self):
        selector = selectors["interval"]
        return self.get_chart_page_element().find_element_by_css_selector(selector).text
