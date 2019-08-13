from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

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
        button = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        button.click()
        self.wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))

    def get_page_element(self):
        return self.driver.find_element_by_css_selector('div#root div.ChartPage_tool__2vx_W')

    def get_search_wrapper_element(self):
        return self.get_page_element().find_element_by_css_selector('div.SearchWithSuggestions_wrapper__3BM6h')

    def get_search_input_element(self):
        return self.get_search_wrapper_element().find_element_by_css_selector('input')

    def get_search_result_element(self, text):
        search_wrapper_element = self.get_search_wrapper_element()
        search_input_element = self.get_search_input_element()
        search_input_element.send_keys(text)
        xpath = "//button[contains(@class, SearchWithSuggestions_suggestion__AqZNi)]//span[text()='{0}']/././.".format(text)
        search_result_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return search_result_element

    def search(self, text):
        self.get_search_result_element(text).click()
        xpath = "//button[contains(@class, SearchWithSuggestions_suggestion__AqZNi)]//span[text()='{0}']/././.".format(text)
        self.wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))

    def get_period_selector_element(self, period):
        xpath = "//div[contains(@class, 'ChartPage_ranges__3h7wX')]//div[text()='{0}']".format(period)
        return self.get_page_element().find_element_by_xpath(xpath)

    def select_period(self, period):
        xpath = "//div[contains(@class, 'Selector_selected__2rsUx') and text()='{0}']".format(period)
        if len(self.get_page_element().find_elements_by_xpath(xpath)) == 0:
            self.get_period_selector_element(period).click()
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def get_metrics_container_element(self):
        return self.get_page_element().find_element_by_css_selector('div.ChartPage_container__2avm9.ChartPage_container_bottom__3Cwyv')

    def get_metrics_categories_element(self):
        return self.get_metrics_container_element().find_element_by_css_selector('div.ChartMetricSelector_column__2SqCU.ChartMetricSelector_categories__uBPiA')

    def get_metrics_category_element(self, category):
        xpath = "//button[contains(text(), '{0}')]".format(category)
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def select_metrics_category(self, category):
        xpath = "//button[contains(text(), '{0}') and contains(@class, 'Button_active__3FPKU')]".format(category)
        if len(self.get_page_element().find_elements_by_xpath(xpath)) == 0:
            self.get_metrics_category_element(category).click()
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def get_metrics_list_element(self):
        selector = 'div.ChartMetricSelector_group__FhAJt'
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def get_metric_element(self, metric):
        xpath = "//button[contains(text(), '{0}')]".format(metric)
        return self.get_metrics_list_element().find_element_by_xpath(xpath)

    def get_active_metrics_panel_element(self):
        selector = 'section.ChartActiveMetrics_wrapper__3Z0I8'
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def get_active_metric_element(self, metric):
        xpath = "//button[contains(text(), '{0}')]".format(metric)
        return self.get_active_metrics_panel_element().find_element_by_xpath(xpath)

    def select_metric(self, metric):
        try:
            self.get_active_metric_element(metric)
        except NoSuchElementException:
            self.select_metrics_category(self.metrics[metric])
            self.get_metric_element(metric).click()
            self.wait.until(EC.visibility_of(self.get_active_metric_element(metric)))

    def deselect_metric(self, metric):
        try:
            active_metric = self.get_active_metric_element(metric)
            active_metric.click()
            self.wait.until(EC.invisibility_of_element(self.get_active_metric_element(metric)))
        except NoSuchElementException:
            pass
