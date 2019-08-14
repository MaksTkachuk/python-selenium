from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import logging
from typing import NamedTuple
from datetime import datetime

class ActiveMetricData(NamedTuple):
    name: str
    active: bool

class Mainpage:

    def __init__(self, driver):
        self.default_url = 'https://app-stage.santiment.net/?from=2019-02-13T21%3A00%3A00.000Z&interval=1d&metrics=historyPrice&slug=bitcoin&title=Bitcoin%20%28BTC%29&to=2019-08-14T21%3A00%3A00.000Z'
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)
        self.metrics = {
        "Price": ("Financial", "historyPrice"),
        "Volume": ("Financial", "volume"),
        "Development Activity": ("Development", "devActivity"),
        "Twitter": ("Social", "historyTwitterData"),
        "Social Volume": ("Social", "socialVolume"),
        "Social Dominance": ("Social", "socialDominance"),
        "Daily Active Deposits": ("On-chain",),
        "Exchange Flow Balance": ("On-chain", "exchangeFundsFlow"),
        "Eth Spent Over Time": ("On-chain", "ethSpentOverTime"),
        "In Top Holders Total": ("On-chain", "topHoldersPercentOfTotalSupply"),
        "Percent of Token Supply on Exchanges": ("On-chain", "percentOfTokenSupplyOnExchanges"),
        "Realized Value": ("On-chain", "realizedValue"),
        "Market Value To Realized Value": ("On-chain", "mvrvRatio"),
        "NVT Ratio Circulation": ("On-chain", "nvtRatioCirculation"),
        "NVT Ratio Transaction Volume": ("On-chain", "nvtRatioTxVolume"),
        "Network Growth": ("On-chain", "networkGrowth"),
        "Daily Active Addresses": ("On-chain", "dailyActiveAddresses"),
        "Token Age Consumed": ("On-chain", "tokenAgeConsumed"),
        "Token Velocity": ("On-chain", "tokenVelocity"),
        "Transaction Volume": ("On-chain", "transactionVolume"),
        "Token Circulation": ("On-chain", "tokenCirculation")
        }
        self.state = {
        "active_metrics": [ActiveMetricData('Price', True)],
        "token": "Bitcoin"
        }
        self.driver.get(self.default_url)

    def close_cookie_popup(self):
        xpath = "//button[text()='Accept']"
        logging.info("Trying to close cookie popup")
        try:
            button = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            button.click()
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            logging.info("Already closed")
        logging.info("Closed successfully")

    def close_explore_popup(self):
        xpath = "//button[text()='Dismiss']"
        logging.info("Trying to close explore assets popup")
        try:
            button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            button.click()
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            logging.info("Already closed")
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
        self.state['token'] = text

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
        if not metric in [x.name for x in self.state['active_metrics']]:
            self.select_metrics_category(self.metrics[metric][0])
            metric_element = self.get_metric_element(metric)
            metric_element.click()
            try:
                self.wait.until(EC.visibility_of(self.get_active_metric_element(metric)))
                self.state['active_metrics'].append(ActiveMetricData(metric, True))
            except TimeoutException:
                xpath = "//span[text()='no data']"
                metric_element.find_element_by_xpath(xpath)
                self.state['active_metrics'].append(ActiveMetricData(metric, False))


    def deselect_metric(self, metric):
        logging.info("Trying to deselect {0} metric".format(metric))
        if ActiveMetricData(metric, True) in self.state['active_metrics']:
            active_metric = self.get_active_metric_element(metric)
            active_metric.click()
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

    def get_graph_title(self):
        return self.get_page_element().find_element_by_css_selector('div.ChartPage_title__fLVYV').text

    def get_from_to_dates(self):
        [date_from_text, date_to_text] = self.get_page_element().find_element_by_css_selector('button.CalendarBtn_btn__2WS5X').text.split('-')
        datetime_from = datetime.strptime(date_from_text.strip(), '%d.%m.%y')
        datetime_to = datetime.strptime(date_to_text.strip(), '%d.%m.%y')
        date_from_converted = datetime.strftime(datetime_from, '%Y-%m-%dT21:00:00.000Z')
        date_to_converted = datetime.strftime(datetime_to, '%Y-%m-%dT21:00:00.000Z')
        return date_from_converted, date_to_converted

    def get_interval(self):
        return self.get_page_element().find_element_by_css_selector('div.Dropdown_wrapper__2SIQh.IntervalSelector_wrapper__3_304').text
