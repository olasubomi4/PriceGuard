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
    def __init__(self,countryCode,productName,currency,driver):
        self.__productName=productName
        self.__currency=currency
        self.__countryCode=countryCode
        self.driver=driver

    def Scrape(self):
        self.driver.get(os.getenv("AMAZON_URL"))
        self._acceptCookies()
        self._changeCountryToDesiredCountry()
        self._changeCurrencyToDesiredCurrency()
        self._findProduct()
        pro= self._getRelevantProducts()

        return pro

    
    def _acceptCookies(self):
        success=False
        counter=0
        while(success==False):
            try:
                if(counter >0):
                    self.driver.get(os.getenv("AMAZON_URL"))
                acceptCookies= WebDriverWait(self.driver,15).until(
                    expected_conditions.presence_of_element_located((By.ID,"sp-cc-accept"))
                )
                acceptCookies.click()
                success=True
            except Exception as e:
                counter += 1
                print(f"Amazon accept cookie retry {counter}")
                if(counter>=4):
                    success=True
    
    def _changeCountryToDesiredCountry(self):
        time.sleep(2)
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

        selectCountry= WebDriverWait(self.driver,25).until(
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


    def _getRelevantProducts(self):
        products= self.driver.find_elements(By.XPATH,"//div[contains(@class, 's-main-slot')]/div[@data-component-type='s-search-result']")

        productList={}

        for product in products:

            try:
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
                productObject.setProductLocation(self.__countryCode)
                productList[productId]=productObject

        time.sleep(5)
        for product in productList.values():
            self._getDetailedInformationAboutProduct(product)

        return productList

    def _getDetailedInformationAboutProduct(self,product):
        if product!=None and product.getProductLink()!=None:
            driver=self.driver
            driver.get(product.getProductLink())
            self._getProuctRating(product,driver)
            self._isProductInStock(product, driver)
            self._getProductFeatures(product,driver)
            self._getDeliveryDetails(product,driver)
            self._getProductDetails(product,driver)
            # self._getProductDetails(product,driver)
            self._getEventName(product,driver)
            self._getDiscountPercentage(product,driver)
            self._getPriceBeforeDiscount(product, driver)
            self._getProductCateogry(product,driver)


    def _getProuctRating(self,product,driver):
        try:
            averageCustomerRating = driver.find_element(By.ID, "averageCustomerReviews")
            averageCustomerRating = averageCustomerRating.find_element(By.XPATH, '//*[@id="acrPopover"]/span[1]/a/span')
            product.setProductRating(averageCustomerRating.text)
        except Exception as e:
            product.setProductRating("Rating not available")

    def _getPriceBeforeDiscount(self,product, driver):
        try:
            priceBeforeDiscount = driver.find_element(By.XPATH, './/*[@id="corePriceDisplay_desktop_feature_div"]/div[2]/span/span[1]/span[2]/span')

            product.setPriceBeforeDiscount(priceBeforeDiscount.text)
        except Exception as e:
            product.setPriceBeforeDiscount(0)

    def _isProductInStock(self,product, driver):
        try:
            productAvailability = driver.find_element(By.ID, "availability")
            productAvailabilityValue = productAvailability.text
            if (productAvailabilityValue == "In stock"):
                product.setIsInStock(True)
        except Exception as e:
                product.setIsInStock("Stock status not available")

    def _seeMoreProductFeatures(self, driver):
        try:
            seeMoreFeatures = WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH,'//*[@id="poToggleButton"]/a'))
            )

            seeMoreFeatures.click()
        except Exception as e:
            print(e)
            pass
    def _getProductFeatures(self,product, driver):
        self._seeMoreProductFeatures(driver)
        try:
            table = WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="poExpander"]/div[1]/div/table/tbody'))
            )
            rows = table.find_elements(By.TAG_NAME, "tr")

            data = {}
            for row in rows:
                try:
                    key_cell = row.find_element(By.CLASS_NAME, "a-span3")
                    value_cell = row.find_element(By.CLASS_NAME, "a-span9")

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
            deliveryInformation = driver.find_element(By.ID, "deliveryBlockMessage");
            product.setDeliveryDetails(deliveryInformation.text)
        except Exception as e:
            product.setDeliveryDetails("Delivery details not available")

    def _getProductDetails(self,product, driver):

        try:
            productDetails = driver.find_element(By.ID, "feature-bullets")
            product.setProductDescription(productDetails.text)
        except Exception as e:
            product.setProductDescription("Product description not available")

    def _getEventName(self,product, driver):
        try:
            product.setEvent(driver.find_element(By.ID, "dealBadgeSupportingText").text)
        except:
            product.setEvent("Event not available")

    def _getDiscountPercentage(self,product, driver):
        try:
            discountPercentage = driver.find_element(By.CLASS_NAME, 'savingPriceOverride')
            product.setDiscountPercentage(discountPercentage.text)
        except:
            product.setDiscountPercentage(None)

    def _getProductCateogry(self,product, driver):
        try:
            productCategory = driver.find_element(By.XPATH, '//*[@id="nav-subnav"]/a[1]/span');
            product.setProductCategory(productCategory.text)
        except Exception as e:
            product.setProductCategory("Product category not available")

    def _extractProductIdFromLink(self,link):
        asin = re.search(r"/dp/([A-Z0-9]{10})",link)
        if asin:
            return asin.group(1)
        return None
    

    
    


        

