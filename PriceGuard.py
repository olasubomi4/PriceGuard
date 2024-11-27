from db.PostgreSql import PostgreSql
from scraper.AmazonScraper import AmazonScraper
import pandas as pd


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
        scrapers = [amazonScraper]
        ps=pd.DataFrame()
        for scraper in scrapers:
            res=scraper.Scrape()
            scraper_json = res.values()

            for a in scraper_json:
                ps = pd.concat([ps, pd.DataFrame([a.to_dict()])], ignore_index=True)

                scrapersResult.append(res)
        ps.to_csv('a.csv',index=False)
        print(ps)

    def performDataTransformation(self):

        pass

    def performDataLoading(self,scrapersResult):
        postgreSql = PostgreSql()
        postgreSql.insertProducts(scrapersResult);
        pass
