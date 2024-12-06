import pandas as pd
import re
from transformer.Transformer import Transformer
from util.Utility import Utility


class EbayPhonesTransformer(Transformer):
    def transformData(self, data: pd.DataFrame):
        data2= data.copy()
        data2.loc[:,"deliveryFee"]=self.__getProductDeliveryFee(data2)
        data2.loc[:,"productLocation"]= self.__getProductLocation(data2)
        data2.loc[:,"earliestDeliveryDate"]=self.__getEarliestDeliveryDate(data2)
        data2.loc[:,"freeDelivery"]=self.__getProductsWithFreeDelivery(data2)
        data2.loc[:,"productRating"]=self.__standardisePrroductRatingOver5(data2)
        # data2["productFeatures"]=data2["productFeatures"]
        data2.loc[:,"brand"]=self.__generateBrandFromProductFeatures(data2)
        data2.loc[:,"operatingSystem"]=self.__generateOperatingSystemFromProductFeatures(data2)
        data2.loc[:,"screenSize"]= self.__generateScreenSizeFromProductFeatures(data2)
        data2.loc[:,"storageCapacity"]= self.__generateProductStorageCapacityFromProductFeatures(data2)
        data2.loc[:,"Colour"]=self.__generateProductColorFromProductFeatures(data2)
        data2.loc[:,"Model"]=self.__generateProductModelFromProductFeatures(data2)
        return data2
    def __generateBrandFromProductFeatures(self, data: pd.DataFrame):
        return data['productFeatures'].apply(lambda x: x.get('Brand'))

    def __generateOperatingSystemFromProductFeatures(self, data: pd.DataFrame):
        return data['productFeatures'].apply(lambda x: x.get('Operating System'))


    def __generateScreenSizeFromProductFeatures(self, data: pd.DataFrame):
        # return data['productFeatures'].get('Screen Size')
        return data['productFeatures'].apply(
        lambda x: x.get('Screen Size'))

    def __generateProductStorageCapacityFromProductFeatures(self, data: pd.DataFrame):
        return data['productFeatures'].apply(lambda x: x.get('Storage Capacity'))
        # return data['productFeatures'].get('Storage Capacity')

    def __generateProductColorFromProductFeatures(self, data: pd.DataFrame):
        # return data['productFeatures'].get('Colour')

        return data['productFeatures'].apply(
            lambda x: x.get('Colour'))

    def __generateProductModelFromProductFeatures(self, data: pd.DataFrame):
        return data['productFeatures'].apply(
            lambda x: x.get('Model'))
        # return data['productFeatures'].get('Model')
    def extractDeliveryFees(self,value):
        postage_pattern = r"Postage|Shipping:\s*(.+)"
        if isinstance(value, str):
            match = re.search(postage_pattern, value)
            if match:
                return match.group(0)
        return None
    def __getProductDeliveryFee(self,data: pd.DataFrame):
        return  self.__getDeliveryFeeInEuros(data['productLocation'].apply(self.extractDeliveryFees))

    def extract_delivery_fee(self,product_location, pattern):
        if product_location is None:
            return None
        if isinstance(product_location, str):
            match = re.search(pattern, product_location)
            return match.group(1) if match else None
        return None

    def __getDeliveryFeeInEuros(self,data):
        return  data.apply(self.extractDeliveryFeesInEuros)

    def extractDeliveryFeesInEuros(self, info):
        if info is None:
            return None
        pattern = r"(?:EUR\s*([0-9]+(?:\.[0-9]{1,2})?)|Free)"
        match = re.search(pattern, info)
        if match:
            return match.group(1) if match.group(1) else 0
        return None

    def extractLocation(self,value):
        located_in_pattern = r"Located in:\s*(.+)"
        if isinstance(value, str):
            match = re.search(located_in_pattern, value)
            if match:
                return match.group(1)
        return None
    def __getProductLocation(self,data: pd.DataFrame):
        return  data['productLocation'].apply(self.extractLocation)

    def extractEarliestDeliveryDate(self, value):
        date_pattern = r"\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b"
        if isinstance(value, str):
            match = re.search(date_pattern, value)
            if match:
                return Utility.predictYearFromDate(match.group(0),"%a, %d %b")
        return None
    def __getEarliestDeliveryDate(self,data: pd.DataFrame):
        a=data['deliveryDetails'].apply(lambda x : self.extractEarliestDeliveryDate(x))
        return a

    def __getProductsWithFreeDelivery(self,data: pd.DataFrame):
        return data['deliveryFee'] == 0


    def __standardisePrroductRatingOver5(self,data: pd.DataFrame):
        ratingInPercentage=self.__extractRatingInPercentage(data)
        if ratingInPercentage is None:
            return None
        ratingInPercentage=ratingInPercentage.str.replace("%","").astype(float)
        return ratingInPercentage/20

    def extractRatingInPercent(self, value):
        percentagePattern= r"\d{1,2}.\d?%"
        if isinstance(value, str):
            match = re.search(percentagePattern, value)
            if match:
                return match.group(0)
        return None
    def __extractRatingInPercentage(self,data: pd.DataFrame):
        return data['productRating'].apply(self.extractRatingInPercent)



    def test(self):
        df= pd.read_csv("/Users/odekunleolasubomi/PycharmProjects/PriceGuard/ab.csv")

        self.transformData(df)


if __name__ == "__main__":
        a= EbayPhonesTransformer()
        a.test()


