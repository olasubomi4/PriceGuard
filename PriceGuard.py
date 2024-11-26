from scraper.AmazonScraper import AmazonScraper


class PriceGuard:
    def __init__(self, countryCode, productName, currency):
        self.__productName = productName
        self.__currency = currency
        self.__countryCode = countryCode

    def performDataAcquisition(self):
        scrapersResult = []
        amazonScraper = AmazonScraper( self.__countryCode,self.__productName, self.__currency)
        scrapers = [amazonScraper]
        for scraper in scrapers:
            res=scraper.Scrape()
            print((res.values()))
            scrapersResult.append(res)

    def performDataTransformation(self):
        pass

    def performDataLoading(self):
        pass
