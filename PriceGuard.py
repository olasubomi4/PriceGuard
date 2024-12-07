from db.PostgreSql import PostgreSql
from factory.AmazonTransformerFactory import AmazonTransformerFactory
from factory.EbayTransformerFactory import EbayTransformerFactory
from scraper.AmazonScraper import AmazonScraper
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os
import numpy as np

from scraper.EbayScraper import EbayScraper
from util.Utility import Utility


class PriceGuard:
    load_dotenv()
    def __init__(self, countryCode, productName, currency,postgresSql:PostgreSql):
        self.__productName = productName
        self.__currency = currency
        self.__countryCode = countryCode
        self.__postgresSql = postgresSql


    def prepareData(self):
        scrapedData1=self.__performDataAcquisition()
        newCopy=scrapedData1.copy()
        a=self.__performDataTransformation(newCopy)
        return self.__performDataLoading(a)

    # def custom_serializer(self,obj):
    #     if hasattr(obj, 'to_dict'):
    #         return obj.to_dict()
    #     raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


    def __performDataAcquisition(self):
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


    def __performDataTransformation(self,scrapedData:  pd.DataFrame):
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

        scrapedData=self.__removeRowsWhereBrandIsNotApple(scrapedData)
        scrapedData=self.__removeRowsWhereColorIsBlank(scrapedData)
        scrapedData=self.__removeRowsWithoutAPrice(scrapedData)
        scrapedData=self.__addBrandNameToModelIfMissing(scrapedData)
        scrapedData=self.__handleMissingScreenSize(scrapedData)
        scrapedData=self.__convertProductPriceToFloat(scrapedData)
        scrapedData=self.__convertPriceBeforeDiscountToFloat(scrapedData)
        scrapedData=self.__standardiseTheScreenSize(scrapedData)
        scrapedData=self.__convertDeliveryFeeToFloat(scrapedData)
        scrapedData=self.__removeProductImageColumn(scrapedData)
        scrapedData=self.__removeOperatingSystemColumn(scrapedData)
        scrapedData=self.__removePercentageSymbolFromDiscountPercentage(scrapedData)
        scrapedData["numberOfDaysTillEarliestDeliveryDate"]=self.__getNumberOfDaystillEarliestDeliveryDate(scrapedData)
        scrapedData=self.__ensureProductRatingValueAsNoMoreThan2Decimal(scrapedData)

        scrapedData.drop(columns=['productFeatures'],inplace=True)
        scrapedData.to_csv('transformedData.csv',index=True)
        return scrapedData

    def __performDataLoading(self,scrapersResult):
        try:
            scrapersResult['id'] = range(1, len(scrapersResult) + 1)
            scrapersResult.set_index('id', inplace=True)
            # scrapersResult=scrapersResult.reset_index(drop=True)
            self.__postgresSql.insertProducts(scrapersResult,self.__productName);
            print("SAVE to db successful")
            return scrapersResult
        except Exception as e:
            print(f"Exception thrown while trying to save result into db {e}")
            return None

    def __removeRowsWhereBrandIsNotApple(self,scrapedData: pd.DataFrame):
        return scrapedData[scrapedData["brand"] == "Apple"]

    def __removeRowsWhereColorIsBlank(self, scrapedData: pd.DataFrame):
        return scrapedData.dropna(subset=["Colour"])

    def __removeRowsWithoutAPrice(self, scrapedData: pd.DataFrame):
        return scrapedData.dropna(subset=["productPrice"])

    def __handleMissingScreenSize(self,ScraperResult: pd.DataFrame):
        modePerModel = ScraperResult.groupby('Model')['screenSize'].apply(
            lambda x: x.mode().iloc[0] if not x.mode().empty else None)
        ScraperResult['screenSize'] = ScraperResult.apply(
            lambda row: modePerModel.get(row['Model'], None) if pd.isnull(row['screenSize']) else row['screenSize'],
            axis=1
        )
        return ScraperResult

    def __addBrandNameToModelIfMissing(self,ScraperResult: pd.DataFrame):
         ScraperResult["Model"]= ScraperResult.apply(lambda row: str(row["brand"])+" "+str(row["Model"]) if str(row["Model"]).split(" ")[0] !=row["brand"] else str(row["Model"]), axis=1)
         return ScraperResult

    def __convertProductPriceToFloat(self,ScraperResult: pd.DataFrame):
        # ScraperResult['productPrice'] = ScraperResult['productPrice'].apply(lambda pr: float(str(pr).replace(",", "")) if isinstance(pr,str)  else None)
        ScraperResult['productPrice'] = ScraperResult['productPrice'].apply(
            lambda pr: pr.replace(",", "") if (isinstance(pr, str)) else None)
        ScraperResult['productPrice'] = ScraperResult['productPrice'].apply(lambda x: Utility.convertStringToFloat(x))
        return ScraperResult

    def __convertPriceBeforeDiscountToFloat(self,ScraperResult: pd.DataFrame):
        # ScraperResult['priceBeforeDiscount'] = ScraperResult['priceBeforeDiscount'].apply(lambda pr: float(str(pr).replace(",", "")) if(isinstance(pr,str) and pr!="Price not available") else None)

        # ScraperResult['priceBeforeDiscount'] = ScraperResult['priceBeforeDiscount'].str.replace(",", "").astype(float)
        ScraperResult['priceBeforeDiscount'] = ScraperResult['priceBeforeDiscount'].apply(
            lambda pr: pr.replace(",", "") if (isinstance(pr, str)) else None)
        ScraperResult['priceBeforeDiscount'] = ScraperResult['priceBeforeDiscount'].apply(lambda x: Utility.convertStringToFloat(x))
        return ScraperResult
    def __convertDeliveryFeeToFloat(self,ScraperResult: pd.DataFrame):
        # ScraperResult['deliveryFee'] = ScraperResult['deliveryFee'].astype(float)
        ScraperResult['deliveryFee'] = ScraperResult['deliveryFee'].apply(lambda pr: pr.replace(",", "") if(isinstance(pr,str)) else None)
        ScraperResult['deliveryFee'] = ScraperResult['deliveryFee'].apply(lambda x: Utility.convertStringToFloat(x))
        return ScraperResult

    def __standardiseTheScreenSize(self,ScraperResult: pd.DataFrame):
        ScraperResult['screenSize'] = ScraperResult["screenSize"].apply(lambda screenSize: screenSize.replace('"', " Inches") if(isinstance(screenSize,str)) else  None)
        ScraperResult['screenSize'] = ScraperResult["screenSize"].apply(lambda screenSize: screenSize.replace(' in', " Inches")if( isinstance(screenSize,str)) else  None)
        return ScraperResult

    def __removeProductImageColumn(self,ScraperResult: pd.DataFrame):
        ScraperResult.drop(columns=['productImage'],inplace=True,axis=1)
        return ScraperResult

    def __removeOperatingSystemColumn(self, ScraperResult: pd.DataFrame):
        ScraperResult.drop(columns=['operatingSystem'], inplace=True,axis=1)
        return ScraperResult

    def __removePercentageSymbolFromDiscountPercentage(self, ScraperResult: pd.DataFrame):
        ScraperResult["discountPercentage"]=ScraperResult["discountPercentage"].apply(lambda x: x.replace("%"," ") if( x!=None and isinstance(x,str)) else None)
        ScraperResult["discountPercentage"]=ScraperResult["discountPercentage"].apply(lambda x: Utility.convertStringToFloat(x))
        return ScraperResult

    def __getNumberOfDaystillEarliestDeliveryDate(self, ScraperResult: pd.DataFrame):
        if 'earliestDeliveryDate' not in ScraperResult.columns or 'productScrapeDate' not in ScraperResult.columns:
            raise ValueError("Required columns are missing from the DataFrame.")

        return ScraperResult.apply( lambda row: Utility.getDayDifferenceBetweenDates(row["earliestDeliveryDate"],row["productScrapeDate"]),axis=1)

    def __ensureProductRatingValueAsNoMoreThan2Decimal(self, ScraperResult: pd.DataFrame):
        ScraperResult["productRating"] = ScraperResult["productRating"].apply(
            lambda x: np.ceil(float(x) * 100) / 100 if (
                        x is not None and pd.notna(x) and float(x) != int(float(x))) else float(x) if pd.notna(x) else x
        )

        return ScraperResult
    # def removeOutlierBrand(self,ScraperResult: pd.DataFrame ):
    #     mostCommonBrand= ScraperResult["brand"].mode()
    #     scrapedData[ScraperResult["brand"]!=mostCommonBrand]


if __name__=="__main__":
    PriceGuard("IE","Iphone 16","EUR",PostgreSql()).prepareData()