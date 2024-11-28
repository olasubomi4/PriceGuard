from db.PostgreSql import PostgreSql
from scraper.AmazonScraper import AmazonScraper
import pandas as pd

from scraper.CurrysScraper import CurrysScraper
from scraper.EbayScraper import EbayScraper


class PriceGuard:
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
        amazonScraper = AmazonScraper( self.__countryCode,self.__productName, self.__currency)
        currysScraper= CurrysScraper( self.__countryCode,self.__productName, self.__currency)
        ebayScraper= EbayScraper( self.__countryCode, self.__productName, self.__currency)
        scrapers = [ebayScraper,amazonScraper]
        ps=pd.DataFrame()
        for scraper in scrapers:
            res=scraper.Scrape()
            scraper_json = res.values()

            for a in scraper_json:
                ps = pd.concat([ps, pd.DataFrame([a.to_dict()])], ignore_index=True)

                scrapersResult.append(res)

        ps.to_csv('a.csv',index=False)
        return ps


    def performDataTransformation(self,scrapedData):
        productCurrency = scrapedData['productCurrency'][0]
        s=scrapedData["priceBeforeDiscount"].str.split(productCurrency,expand=True)
        if(s[0] is None):
            scrapedData["priceBeforeDiscount"]=s[1]
        else:
            scrapedData["priceBeforeDiscount"]="n/a"


        print(s);

        pass

    def performDataLoading(self,scrapersResult):
        postgreSql = PostgreSql()
        postgreSql.insertProducts(scrapersResult);
        pass
