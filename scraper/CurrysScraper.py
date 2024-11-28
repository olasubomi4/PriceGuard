import time

from dto.Product import Product

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import re;
import os

from scraper.Scraper import Scraper
class CurrysScraper(Scraper):
    load_dotenv()
    service = Service(executable_path=os.getenv("EXE_PATH"))
    driver = webdriver.Chrome(service=service)

    def __init__(self, countryCode, productName, currency):
        self.__productName = productName
        self.__currency = currency
        self.__countryCode = countryCode


    def Scrape(self):
        self.driver.get(os.getenv("CURRYS_URL"))
        time.sleep(6)
        self._acceptCookies()
        time.sleep(2)
        self._findProduct()
        time.sleep(2)

        # self._acceptCookies()
        # self._changeCountryToDesiredCountry()
        # self._changeCurrencyToDesiredCurrency()
        # self._findProduct()
        # return self._getRelevantProducts()

    def _acceptCookies(self):
        acceptCookies= WebDriverWait(self.driver,15).until(
            expected_conditions.presence_of_element_located((By.ID,"onetrust-accept-btn-handler"))
        )
        acceptCookies.click()

    def _findProduct(self):
        time.sleep(5)
        searchBox= WebDriverWait(self.driver,17).until(
            expected_conditions.presence_of_element_located((By.ID,"Search"))
        )
        searchBox.send_keys(self.__productName)
        time.sleep(5)
        searchBox.submit()