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


class AmazonScraper(Scraper):
    load_dotenv()
    service= Service(executable_path=os.getenv("EXE_PATH"))
    driver=webdriver.Chrome(service=service)
    def __init__(self,countryCode,productName,currency):
        self.__productName=productName
        self.__currency=currency
        self.__countryCode=countryCode

    def Scrape(self):
        self.driver.get(os.getenv("AMAZON_URL"))
        self._acceptCookies()
        self._changeCountryToDesiredCountry()
        self._changeCurrencyToDesiredCurrency()
        self._findProduct()
        return self._getRelevantProductLinks()

    
    def _acceptCookies(self):
        acceptCookies= WebDriverWait(self.driver,15).until(
            expected_conditions.presence_of_element_located((By.ID,"sp-cc-accept"))
        )
        acceptCookies.click()
    
    def _changeCountryToDesiredCountry(self):
        changeCountry=WebDriverWait(self.driver,15).until(
            expected_conditions.presence_of_element_located((By.ID,"nav-global-location-popover-link"))

        )
        changeCountry.click()

        selectCountry= WebDriverWait(self.driver,15).until(
            expected_conditions.presence_of_element_located((By.ID,"GLUXCountryValue"))
        )

        selectCountry.click()

        selectDesiredCoutry =WebDriverWait(self.driver,15).until(
            expected_conditions.presence_of_element_located((By.XPATH, f"//a[@data-value='{{\"stringVal\":\"{self.__countryCode}\"}}']"))
        )
        selectDesiredCoutry.click()

    def _changeCurrencyToDesiredCurrency(self):
        changeCurrency= WebDriverWait(self.driver,15).until(
            expected_conditions.element_to_be_clickable((By.ID,"icp-touch-link-cop"))
        )
        changeCurrency.click()

        changeCurrencyDropDownButton=WebDriverWait(self.driver,15).until(
            expected_conditions.element_to_be_clickable((By.ID,"icp-currency-dropdown-selected-item-prompt"))

        )
        changeCurrencyDropDownButton.click()

        selectCountry= WebDriverWait(self.driver,15).until(
            expected_conditions.element_to_be_clickable((By.ID,self.__currency))
        )

        selectCountry.click()

        saveSelectedCountry=WebDriverWait(self.driver,15).until(
            expected_conditions.element_to_be_clickable((By.XPATH,'.//*[@id="icp-save-button"]/span/input'))

        )
        saveSelectedCountry.click()
    def _findProduct(self):
        time.sleep(5)
        searchBox= WebDriverWait(self.driver,10).until(
            expected_conditions.presence_of_element_located((By.ID,"twotabsearchtextbox"))
        )
        searchBox.send_keys(self.__productName)
        time.sleep(5)
        searchBox.submit()


    def _getRelevantProductLinks(self):
        products= self.driver.find_elements(By.XPATH,"//div[contains(@class, 's-main-slot')]/div[@data-component-type='s-search-result']")

        productList={}

        for product in products:

            try:
                title= product.find_element(By.XPATH,".//span[@class='a-size-medium a-color-base a-text-normal']").text
                title= product.find_element(By.XPATH,".//span[@class='a-size-medium a-color-base a-text-normal']").text

                if(self.__productName.lower() not in title.lower()):
                    continue
            except:
                title="Title not found"
            
            try:
                price= product.find_element(By.XPATH,".//span[@class='a-price-whole']").text
            except:
                price ="Price not available"

            try:
                currency= product.find_element(By.XPATH,".//span[@class='a-price-symbol']").text
            except:
                currency= "Currency not available"

            try:
                link = product.find_element(By.XPATH,".//a[@class='a-link-normal s-no-outline']").get_attribute("href")
            except:
                link= "Link not available"

            productId = self._extractProductIdFromLink(link)
            if productId!=None:
                productObject= Product("AMAZON")
                productObject.setProductLink(link)
                productObject.setProductId(productId)
                productObject.setProductPrice(price)
                productObject.setProductName(title)
                productObject.setProductCurrency(currency)
                productList[productId]=productObject

        return productList

    def _extractProductIdFromLink(self,link):
        asin = re.search(r"/dp/([A-Z0-9]{10})",link)
        if asin:
            return asin.group(1)
        return None
    

    
    


        

