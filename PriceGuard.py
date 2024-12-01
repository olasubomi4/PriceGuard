from db.PostgreSql import PostgreSql
from factory.AmazonTransformerFactory import AmazonTransformerFactory
from factory.EbayTransformerFactory import EbayTransformerFactory
from scraper.AmazonScraper import AmazonScraper
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import re;
import os

from scraper.CurrysScraper import CurrysScraper
from scraper.EbayScraper import EbayScraper


class PriceGuard:
    load_dotenv()
    def __init__(self, countryCode, productName, currency):
        self.__productName = productName
        self.__currency = currency
        self.__countryCode = countryCode


    def custom_serializer(self,obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


    def performDataAcquisition(self):
        scrapersResult = []
        service = Service(executable_path=os.getenv("EXE_PATH"))
        driver = webdriver.Chrome(service=service)
        amazonScraper = AmazonScraper( self.__countryCode,self.__productName, self.__currency,driver)
        ebayScraper= EbayScraper( self.__countryCode, self.__productName, self.__currency,driver)
        scrapers = [amazonScraper,ebayScraper]
        ps=pd.DataFrame()
        for scraper in scrapers:
            res=scraper.Scrape()
            scraper_json = res.values()

            for a in scraper_json:
                ps = pd.concat([ps, pd.DataFrame([a.to_dict()])], ignore_index=True)
                scrapersResult.append(res)

        ps.to_csv('rawData.csv',index=True)
        return ps


    def performDataTransformation(self,scrapedData:  pd.DataFrame):
        ebayData = scrapedData[scrapedData["productStore"] == "Ebay"]
        amazonData = scrapedData[scrapedData["productStore"] == "AMAZON"]
        scrapedData = scrapedData[scrapedData["productStore"] != "Ebay"]
        scrapedData = scrapedData[scrapedData["productStore"] != "AMAZON"]
        ebayTransformer=EbayTransformerFactory().createTransformer(self.__productName)
        amazonTransformer=AmazonTransformerFactory().createTransformer(self.__productName)

        all_data = []
        all_data.append(ebayTransformer.transformData(ebayData))
        all_data.append(amazonTransformer.transformData(amazonData))
        # scrapedData=pd.concat([scrapedData,ebayTransformer.transformData(ebayData)],ignore_index=True)
        scrapedData=pd.concat(all_data,ignore_index=True)



        scrapedData.to_csv('transformedData.csv',index=True)

        scrapedData=self.removeRowsWhereBrandIsNotApple(scrapedData)
        scrapedData=self.removeRowsWhereColorIsBlank(scrapedData)


        print("ad")

    def performDataLoading(self,scrapersResult):
        postgreSql = PostgreSql()
        postgreSql.insertProducts(scrapersResult);

        pass


    def removeRowsWhereBrandIsNotApple(self,scrapedData: pd.DataFrame):
        brandsWhichAreNotApple= scrapedData[scrapedData["brand"] != "Amazon"]
        return scrapedData

    def removeRowsWhereColorIsBlank(self, scrapedData: pd.DataFrame):
        return scrapedData.dropna(subset=["Colour"])