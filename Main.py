from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv
import os

load_dotenv();

def acceptCookies():
    acceptCookies=driver.find_element(By.ID,"sp-cc-accept");
    acceptCookies.click()

def changeCountryToIreland():
    changeCountry=driver.find_element(By.ID,"nav-global-location-popover-link");
    changeCountry.click()
    

    selectCoutry= driver.find_element(By.ID,"GLUXCountryValue")
    selectCoutry.click()

    selectIreland=driver.find_element(By.ID,"GLUXCountryList_4");
    selectIreland.click()

def findAProduct(productName):
    searchBox=WebDriverWait(driver,10).until(
       EC.visibility_of_element_located((By.ID,"twotabsearchtextbox"))
    )
    # searchBox=driver.find_element(By.ID,"twotabsearchtextbox")
    searchBox.send_keys(productName);
    searchBox.submit();


sbr_connection= ChromiumRemoteConnection( os.getenv("SBR_WEBDRIVER"),"goog","chrome")
with Remote(sbr_connection,options=ChromeOptions()) as driver:
    driver.get("https://www.amazon.co.uk")


    acceptCookies();
    changeCountryToIreland();
    findAProduct("Macbook");
    
   
    time.sleep(15)


