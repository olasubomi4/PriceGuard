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
class EbayScraper(Scraper):
    load_dotenv()
    service = Service(executable_path=os.getenv("EXE_PATH"))
    driver = webdriver.Chrome(service=service)

    def __init__(self, countryCode, productName, currency):
        self.__productName = productName
        self.__currency = currency
        self.__countryCode = countryCode


    def Scrape(self):
        self.driver.get(os.getenv("EBAY_URL"))
        time.sleep(6)
        self._acceptCookies()
        time.sleep(2)
        self._findProduct()
        time.sleep(2)
        self._filterProductConditionToBrandNew();
        return self._getRelevantProducts()


    def _acceptCookies(self):
        acceptCookies= WebDriverWait(self.driver,15).until(
            expected_conditions.presence_of_element_located((By.ID,"gdpr-banner-accept"))
        )
        acceptCookies.click()

    def _findProduct(self):
        time.sleep(5)
        searchBox= WebDriverWait(self.driver,17).until(
            expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="gh-ac"]'))
        )
        searchBox.send_keys(self.__productName)
        time.sleep(5)
        searchBox.submit()

    def _getRelevantProducts(self):

        productsContainer = self.driver.find_elements(By.ID,
                                             'srp-river-results')[0]

        products = productsContainer.find_elements(By.XPATH, ".//li[contains(@class, 's-item')]")

        #

        productList = {}

        for product in products:
            try:
                title = product.find_element(By.CLASS_NAME,
                                             "s-item__title").text

                if (self.__productName.lower() not in title.lower()):
                    continue
            except:
                title = "Title not found"

            try:
                currency,price = product.find_element(By.CLASS_NAME, "s-item__price").text.split()
            except:
                price = "Price not available"
                currency = "Currency not available"


            try:
                link = product.find_element(By.CLASS_NAME, "s-item__link").get_attribute("href")
            except:
                link = "Link not available"

            productId = self._extractProductIdFromLink(link)
            if productId != None:
                productObject = Product("Ebay")
                productObject.setProductLink(link)
                productObject.setProductId(productId)
                productObject.setProductPrice(price)
                productObject.setProductName(title)
                productObject.setProductCurrency(currency)
                productList[productId] = productObject

        time.sleep(5)
        for product in productList.values():
            self._getDetailedInformationAboutProduct(product)

        return productList

    def _getDetailedInformationAboutProduct(self, product):
        if product != None and product.getProductLink() != None:
            driver = self.driver
            driver.get(product.getProductLink())
            # self._getProuctRating(product, driver)
            self._isProductInStock(product, driver)
            self._getProductLocation(product, driver)
            self._getProductFeatures(product, driver)
            self._getDeliveryDetails(product, driver)
            self._getProductDetails(product, driver)
            self._getEventName(product, driver)
            self._getProductCateogry(product, driver)


            time.sleep(2)


            # self._getDiscountPercentage(product, driver)
            # self._getPriceBeforeDiscount(product, driver)
            # self._getProductCateogry(product, driver)
            # self._getProductLocation(product, driver)



    def _isProductInStock(self,product, driver):
        try:
            productAvailability = driver.find_element(By.ID, "qtyAvailability")
            productAvailabilityValue = int(productAvailability.text.split(" ")[0])

            if (productAvailabilityValue>0):
                product.setIsInStock(True)
        except Exception as e:
                product.setIsInStock("Stock status not available")

    def _getProductLocation(self,product, driver):
        try:
            productLocation = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[1]/div[8]/div/div/div/div[2]/div/div/div[2]/div/div[2]/span')
            productLocationValue = productLocation.text.split(":")[1]
            product.setProductLocation(productLocationValue)

        except Exception as e:
            product.setProductLocation("Product location not available")

    def _getProductFeatures(self, product, driver):
        try:
            table = WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.ID, 'viTabs_0_is'))
            )
            rows = table.find_elements(By.TAG_NAME, "dl")

            data = {}
            for row in rows:
                try:
                    key_cell = row.find_element(By.TAG_NAME, "dt")
                    value_cell = row.find_element(By.TAG_NAME, "dd")

                    key = key_cell.text.strip()
                    value = value_cell.text.strip()

                    data[key] = value
                except Exception as e:
                    continue

            for key, value in data.items():
                print(f"{key}: {value}")

            product.setProductFeatures(data)
        except:
            product.setProductFeatures("Features not available")

    def _getDeliveryDetails(self,product, driver):
        try:
            deliveryDetails= driver.find_element(By.XPATH,'//*[@id="mainContent"]/div/div[8]/div/div/div/div[3]/div/div/div/div[2]').text
            product.setDeliveryDetails(deliveryDetails)

        except Exception as e:
            product.setDeliveryDetails("Delivery details not available")

            # self._getProductDetails(product, driver)
    def _getProductDetails(self,product, driver):
        try:
            productDetailsIframe= driver.find_element(By.ID,'desc_ifr')
            driver.switch_to.frame(productDetailsIframe)
            productDetails= driver.find_elements(By.TAG_NAME, "body")
            a=productDetails[0]

            product.setProductDescription(a.text)
            driver.switch_to.default_content()


        except Exception as e:
            product. setProductDescription("Product details not available")

    def _getEventName(self,product, driver):
        product.setEvent("Event name not available")

    def _getProductCateogry(self, product, driver):
        try:
            productCategory = driver.find_element(By.XPATH, '/html/body/div[2]/main/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div/nav/ul/li[3]/a/span');
            product.setProductCategory(productCategory.text)
        except Exception as e:
            product.setProductCategory("Product category not available")
    def _filterProductConditionToBrandNew(self,):
        time.sleep(2)
        productCondition = self.driver.find_element(By.XPATH, "//input[@aria-label='New']")
        productCondition.click()
        time.sleep(2)
        # brandNewProductCondition= driver.find_element()

    def _extractProductIdFromLink(self, link):
        asin = re.search(r"/itm/([A-Z0-9]{12})", link)
        if asin:
            return asin.group(1)
        return None

    def _getProuctRating(self, product, driver):
        try:
            averageCustomerRating = driver.find_element(By.ID, "averageCustomerReviews")
            averageCustomerRating = averageCustomerRating.find_element(By.XPATH, '//*[@id="acrPopover"]/span[1]/a/span')
            product.setProductRating(averageCustomerRating.text)
        except Exception as e:
            product.setProductRating("Rating not available")
