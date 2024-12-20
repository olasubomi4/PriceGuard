import pickle
import time
from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor

from selenium.common import NoSuchElementException

from dto.Product import Product

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import re;
from math import ceil
import multiprocessing
import os

from scraper.Scraper import Scraper
# from util.EbayScraperHelper import EbayScraperHelper


class EbayScraper(Scraper):
    load_dotenv()
    # service = Service(executable_path=os.getenv("EXE_PATH"))
    # driver = webdriver.Chrome(service=service)

    def __init__(self, countryCode, productName, currency,driver):
        self.__productName = productName
        self.__currency = currency
        self.__countryCode = countryCode
        self.driver = driver


    def Scrape(self):
        time.sleep(6)
        self.driver.get(os.getenv("EBAY_URL"))
        time.sleep(6)
        self._acceptCookies()
        time.sleep(2)
        self._findProduct()
        time.sleep(2)
        self._filterProductConditionToBrandNew();
        return self._getRelevantProducts()


    def _acceptCookies(self):
        success=False
        counter=0
        while(success==False):
            try:
                if(counter>0):
                    self.driver.get(os.getenv("EBAY_URL"))
                acceptCookies = WebDriverWait(self.driver, 15).until(
                    expected_conditions.presence_of_element_located((By.ID, "gdpr-banner-accept"))
                )
                acceptCookies.click()
                success=True
            except Exception as e:
                counter += 1
                print(f"Ebay accept cookie retry {counter}")
                if(counter>=4):
                    success=True

    def _findProduct(self):
        time.sleep(5)
        searchBox= WebDriverWait(self.driver,17).until(
            expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="gh-ac"]'))
        )
        searchBox.send_keys(self.__productName)
        time.sleep(5)
        searchBox.submit()

    def _getRelevantProducts(self):
        counter=1
        productList = {}
        limit= int(os.getenv("EBAY_PAGE_LIMIT"))
        while limit > counter:

            productsContainer = self.driver.find_elements(By.ID,
                                                 'srp-river-results')[0]

            products = productsContainer.find_elements(By.XPATH, ".//li[contains(@class, 's-item')]")

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

            self._goToNextPage(self.driver)
            counter+=1
            time.sleep(5)
            # EbayScraperHelper.getDetailedInformationAboutProductWhileUtilisingParallelism(self, productList)
        self.__getDetailedInformationAboutProductWhileUtilisingParallelism(productList)
        # for product in productList.values():
        #     self._getDetailedInformationAboutProduct(product)

        return productList


    def __getDetailedInformationAboutProductWhileUtilisingParallelism(self, productList:dict):
        chunksList=self.__splitProductListIntoChunks(productList);
        processList=[]
        # self.driver.quit()
        processResultList=[]
        processResultDic={}
        # multiprocessing.set_start_method('fork')
        numberOfThreads = int(os.getenv("NUMBER_OF_THREADS",1))
        with ThreadPoolExecutor(max_workers=numberOfThreads) as executor:
            for chunks in chunksList:
                # serializedChunks = pickle.dumps(chunks)
                processList.append(
                    executor.submit(self.__executeGetProductDetailsWithAProcess, chunks))

            for future in as_completed(processList):
                processResultList.append(future.result())
            #
            # for processResult in processResultList:
            #     processResultDic.update(processResult)
            # return processResultDic



        # processResultDic={}
        # for chunks in chunksList:
        #     driver=self.__createANewSeleniumDriver()
        #     process = multiprocessing.Process(target=EbayScraper.__executeGetProductDetailsWithAProcess, args=(self,chunks,driver))
        #     processList.append(process)
        #
        # for process in processList:
        #     process.start()
        #
        # for process in processList:
        #     processResultList.append(process.join())

        # for processResult in processResultList:
        #     processResultDic.update(processResult)
        # return processResultDic

    def __executeGetProductDetailsWithAProcess(self, productList):
        driver= self.__createANewSeleniumDriver()
        # productList = pickle.loads(seralizedProductList)
        for product in productList.values():
            self._getDetailedInformationAboutProduct(product,driver)
        # return productList


    def __splitProductListIntoChunks(self, productList:dict):
        numberOfCores = int(os.getenv("NUMBER_OF_THREADS",1))
        chunkSize=ceil(len(productList)/numberOfCores)
        chunkList=[]
        chunkDictionary={}
        for i,(key,value) in enumerate(productList.items()):
            chunkDictionary[key]=value
            if (i+1)%chunkSize ==0 or i+1 == len(productList):
                chunkList.append(chunkDictionary)
                chunkDictionary={}
        return chunkList



    def _getDetailedInformationAboutProduct(self, product,driver):

        if product != None and product.getProductLink() != None:
            try:
                # driver = self.driver
                driver.get(product.getProductLink())
                self._getProuctRating(product, driver)
                self._isProductInStock(product, driver)
                self._getProductLocation(product, driver)
                self._getProductFeatures(product, driver)
                self._getDeliveryDetails(product, driver)
                self._getProductDetails(product, driver)
                self._getEventName(product, driver)
                self._getProductCateogry(product, driver)
            except Exception as e:
                print(e)



            time.sleep(2)




    def _isProductInStock(self,product, driver):
        try:
            productAvailability = driver.find_element(By.XPATH, '//*[@id="qtyTextBox"]')
            # productAvailabilityValue = int(productAvailability.text.split(" ")[0])
            productAvailabilityValue = int(productAvailability.get_attribute("value"))


            if (productAvailabilityValue>0):
                product.setIsInStock(True)
        except Exception as e:
                product.setIsInStock(True)

    def _getProductLocation(self,product, driver):
        try:
            # // *[ @ id = "mainContent"] / div / div[7] / div / div / div / div[1] / div / div / div[2] / div / div[
            #     2] / span
            # // *[ @ id = "mainContent"] / div[1] / div[8] / div / div / div / div[1] / div / div / div[2] / div / div[
            #     2] / span
            productLocation = driver.find_element(By.XPATH,'//div[contains(@class, "ux-labels-values--shipping")]')
            productLocationValue = productLocation.text
            product.setProductLocation(productLocationValue)

        except Exception as e:
            # try :
            #     productLocation = driver.find_element(By.XPATH,
            #                                           '//*[@id="mainContent"]/div/div[6]/div/div/div/div[1]/div/div/div[2]/div/div[2]/span')
            #     productLocationValue = productLocation.text.split(":")[1]
            #     product.setProductLocation(productLocationValue)
            # except Exception as e:
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
            product.setProductFeatures({})

    def _getDeliveryDetails(self,product, driver):
        try:
            deliveryDetails= driver.find_element(By.XPATH,'//div[contains(@class, "deliverto")]').text
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
        product.setEvent("Event not available")

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

    def _goToNextPage(self,driver):
        try:
            nextPage = driver.find_element(By.CLASS_NAME, "pagination__next")
            nextPage.click()
        except Exception as e:
            print(e)
        # driver.get(nextPage)


    def _getProuctRating(self, product, driver):
        try:
            averageCustomerRating = driver.find_element(By.XPATH, '//*[@id="STORE_INFORMATION"]/div/div/div[1]/div[1]/div[2]/div/h4/span[1]')
            product.setProductRating(averageCustomerRating.text)
        except Exception as e:
            product.setProductRating("Rating not available")

    def __createANewSeleniumDriver(self):
        service = Service(executable_path=os.getenv("EXE_PATH"))
        driver = webdriver.Chrome(service=service)
        return driver