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
from util.Utility import Utility


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

        scrapedData=self.removeRowsWhereBrandIsNotApple(scrapedData)
        scrapedData=self.removeRowsWhereColorIsBlank(scrapedData)
        scrapedData=self.removeRowsWithoutAPrice(scrapedData)
        scrapedData=self.addBrandNameToModelIfMissing(scrapedData)
        scrapedData=self.handleMissingScreenSize(scrapedData)
        scrapedData=self.convertProductPriceToFloat(scrapedData)
        scrapedData=self.convertPriceBeforeDiscountToFloat(scrapedData)
        scrapedData=self.standardiseTheScreenSize(scrapedData)
        scrapedData=self.convertDeliveryFeeToFloat(scrapedData)
        scrapedData=self.removeProductImageColumn(scrapedData)
        scrapedData=self.removeOperatingSystemColumn(scrapedData)
        scrapedData=self.removePercentageSymbolFromDiscountPercentage(scrapedData)
        scrapedData["numberOfDaysTillEarliestDeliveryDate"]=self.getNumberOfDaystillEarliestDeliveryDate(scrapedData)


        scrapedData.drop(columns=['productFeatures'],inplace=True)
        scrapedData.to_csv('transformedData.csv',index=True)
        return scrapedData

    def performDataLoading(self,scrapersResult):
        try:
            postgreSql = PostgreSql()
            postgreSql.insertProducts(scrapersResult,self.__productName);
            print("SAVE to db successfull")
        except Exception as e:
            print(f"Exception thrown while trying to save result into db {e}")

        pass


    def removeRowsWhereBrandIsNotApple(self,scrapedData: pd.DataFrame):
        return scrapedData[scrapedData["brand"] == "Apple"]

    def removeRowsWhereColorIsBlank(self, scrapedData: pd.DataFrame):
        return scrapedData.dropna(subset=["Colour"])

    def removeRowsWithoutAPrice(self, scrapedData: pd.DataFrame):
        return scrapedData.dropna(subset=["productPrice"])

    def handleMissingScreenSize(self,ScraperResult: pd.DataFrame):
        modePerModel = ScraperResult.groupby('Model')['screenSize'].apply(
            lambda x: x.mode().iloc[0] if not x.mode().empty else None)
        ScraperResult['screenSize'] = ScraperResult.apply(
            lambda row: modePerModel.get(row['Model'], None) if pd.isnull(row['screenSize']) else row['screenSize'],
            axis=1
        )
        return ScraperResult

    def addBrandNameToModelIfMissing(self,ScraperResult: pd.DataFrame):
         ScraperResult["Model"]= ScraperResult.apply(lambda row: str(row["brand"])+" "+str(row["Model"]) if str(row["Model"]).split(" ")[0] !=row["brand"] else str(row["Model"]), axis=1)
         return ScraperResult

    def convertProductPriceToFloat(self,ScraperResult: pd.DataFrame):
        # ScraperResult['productPrice'] = ScraperResult['productPrice'].apply(lambda pr: float(str(pr).replace(",", "")) if isinstance(pr,str)  else None)
        ScraperResult['productPrice'] = ScraperResult['productPrice'].apply(
            lambda pr: pr.replace(",", "") if (isinstance(pr, str)) else None)
        ScraperResult['productPrice'] = ScraperResult['productPrice'].apply(lambda x: Utility.convertStringToFloat(x))
        return ScraperResult

    def convertPriceBeforeDiscountToFloat(self,ScraperResult: pd.DataFrame):
        # ScraperResult['priceBeforeDiscount'] = ScraperResult['priceBeforeDiscount'].apply(lambda pr: float(str(pr).replace(",", "")) if(isinstance(pr,str) and pr!="Price not available") else None)

        # ScraperResult['priceBeforeDiscount'] = ScraperResult['priceBeforeDiscount'].str.replace(",", "").astype(float)
        ScraperResult['priceBeforeDiscount'] = ScraperResult['priceBeforeDiscount'].apply(
            lambda pr: pr.replace(",", "") if (isinstance(pr, str)) else None)
        ScraperResult['priceBeforeDiscount'] = ScraperResult['priceBeforeDiscount'].apply(lambda x: Utility.convertStringToFloat(x))
        return ScraperResult
    def convertDeliveryFeeToFloat(self,ScraperResult: pd.DataFrame):
        # ScraperResult['deliveryFee'] = ScraperResult['deliveryFee'].astype(float)
        ScraperResult['deliveryFee'] = ScraperResult['deliveryFee'].apply(lambda pr: pr.replace(",", "") if(isinstance(pr,str)) else None)
        ScraperResult['deliveryFee'] = ScraperResult['deliveryFee'].apply(lambda x: Utility.convertStringToFloat(x))
        return ScraperResult

    def standardiseTheScreenSize(self,ScraperResult: pd.DataFrame):
        ScraperResult['screenSize'] = ScraperResult["screenSize"].apply(lambda screenSize: screenSize.replace('"', " Inches") if(isinstance(screenSize,str)) else  None)
        ScraperResult['screenSize'] = ScraperResult["screenSize"].apply(lambda screenSize: screenSize.replace(' in', " Inches")if( isinstance(screenSize,str)) else  None)
        return ScraperResult

    def removeProductImageColumn(self,ScraperResult: pd.DataFrame):
        ScraperResult.drop(columns=['productImage'],inplace=True,axis=1)
        return ScraperResult

    def removeOperatingSystemColumn(self, ScraperResult: pd.DataFrame):
        ScraperResult.drop(columns=['operatingSystem'], inplace=True,axis=1)
        return ScraperResult

    def removePercentageSymbolFromDiscountPercentage(self, ScraperResult: pd.DataFrame):
        ScraperResult["discountPercentage"]=ScraperResult["discountPercentage"].apply(lambda x: x.replace("%"," ") if( x!=None and isinstance(x,str)) else None)
        ScraperResult["discountPercentage"]=ScraperResult["discountPercentage"].apply(lambda x: Utility.convertStringToFloat(x))
        return ScraperResult

    def getNumberOfDaystillEarliestDeliveryDate(self, ScraperResult: pd.DataFrame):
        if 'earliestDeliveryDate' not in ScraperResult.columns or 'productScrapeDate' not in ScraperResult.columns:
            raise ValueError("Required columns are missing from the DataFrame.")

        return ScraperResult.apply( lambda row: Utility.getDayDifferenceBetweenDates(row["earliestDeliveryDate"],row["productScrapeDate"]),axis=1)

    # def removeOutlierBrand(self,ScraperResult: pd.DataFrame ):
    #     mostCommonBrand= ScraperResult["brand"].mode()
    #     scrapedData[ScraperResult["brand"]!=mostCommonBrand]