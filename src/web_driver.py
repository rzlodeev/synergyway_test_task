# Selenium web driver file
import requests

import pandas as pd
from io import StringIO

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

from selenium.common.exceptions import NoSuchElementException


class FirefoxWebDriver:
    """
    Selenium web driver driven by Firefox.
    Makes corresponding API calls to get user data and credit card data.
    Pass "user_data_link" and "credit_card_data_link" when initializing as kwargs
    to set links for those APIs.
    """
    def __init__(self, **kwargs):
        firefox_options = Options()
        firefox_options.add_argument('--headless')  # Do not open browser window

        self.driver = webdriver.Firefox(options=firefox_options)

        self.user_data_link = kwargs.get("user_data_link")
        self.credit_card_data_link = kwargs.get("credit_card_data_link")
        self.addresses_data_link = kwargs.get("addresses_data_link")

    def _get_table_data(self, table_link: str) -> dict:
        """
        Extracts data from HTML tables.
        :param table_link: Link to a web page that consists table.
        :return: Dict with extracted data.
        """
        try:
            # Login to random-data-api.com first
            if 'random-data-api.com' in table_link:
                self.driver.get('https://random-data-api.com/developers/sign_in')

                # Proceed if warning of already sign-in not found
                if not self.driver.find_elements(
                        By.XPATH, "//div[@class='toast-body' and contains(text(), 'You are already signed in.')]"):

                    # Type in email
                    email_input = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.ID, 'developer_email'))
                    )
                    email_input.clear()
                    email_input.send_keys('testemail@ex.com')

                    # Type in password
                    password_input = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.ID, "developer_password"))
                    )
                    password_input.clear()
                    password_input.send_keys('testpassword')

                    # Wait until the submit button is clickable and click it
                    submit_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@value='Go to dashboard']"))
                    )
                    submit_button.click()

                    # Wait until 'Log out' button appears to make sure we logged in
                    WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//div[@class='toast-body' and contains(text(), 'Signed in successfully.')]"))
                    )

            self.driver.get(table_link)

            # Extract <table> tag and save it as HTML text.
            api_response_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'table'))
            )
            raw_html = api_response_element.get_attribute('outerHTML')

            # Convert HTML table to dict
            df = pd.read_html(StringIO(raw_html))[0]
            final = df.to_dict(orient='index')

            return final

        except NoSuchElementException:
            raise Exception("Element with data not found. Please ensure that element "
                            "Xpath with data on the source page "
                            "matches path inside the script, where it tries to find it.")

    def get_user_data(self) -> dict:
        """
        Extracts user data from corresponding API using requests.
        :return: Dict with extracted user data
        """
        try:
            response = requests.get(self.user_data_link)
            return response.json()
        except Exception as e:
            raise e

    def get_credit_card_data(self) -> dict:
        """
        Extracts credit card from corresponding API.
        :return: Dict with extracted credit card data.
        """
        if self.credit_card_data_link:
            credit_card_dict = self._get_table_data(self.credit_card_data_link)
        else:
            raise Exception("Link for credit card data API is not configured.")

        return credit_card_dict

    def get_addresses_data(self) -> dict:
        """
            Extracts addresses from corresponding API.
            :return: Dict with extracted addresses data.
            """
        if self.addresses_data_link:
            addresses_dict = self._get_table_data(self.addresses_data_link)
        else:
            raise Exception("Link for addresses data API is not configured.")

        return addresses_dict
