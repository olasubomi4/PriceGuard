import pandas as pd
import re
from transformer.Transformer import Transformer
from util.Utility import Utility


class AmazonTransformer (Transformer):
    def transformData(self, data: pd.DataFrame):
        data.loc[:,"deliveryFee"] = self.__getProductDeliveryFee(data)
        # data["productLocation"] = self.__getProductLocation(data)
        data.loc[:,"earliestDeliveryDate"] =self.__getEarliestDeliveryDate(data)
        data.loc[:,"freeDelivery"] = self.__getProductsWithFreeDelivery(data)
        data.loc[:,"brand"]=self.__generateBrandFromProductFeatures(data)
        data.loc[:,"operatingSystem"]=self.__generateOperatingSystemFromProductFeatures(data)
        data.loc[:,"screenSize"]= self.__generateScreenSizeFromProductFeatures(data)
        data.loc[:,"storageCapacity"]= self.__generateProductStorageCapacityFromProductFeatures(data)
        data.loc[:,"Colour"]=self.__generateProductColorFromProductFeatures(data)
        data.loc[:,"Model"]=self.__generateProductModelFromProductFeatures(data)
        return data
    def __generateBrandFromProductFeatures(self, data: pd.DataFrame):
        return data['productFeatures'].apply(lambda x: x.get('Brand'))

    def __generateOperatingSystemFromProductFeatures(self, data: pd.DataFrame):
        # return data['productFeatures'].get('Operating system')
        return data['productFeatures'].apply(lambda x: x.get('Operating system'))

    def __generateScreenSizeFromProductFeatures(self, data: pd.DataFrame):
        # return data['productFeatures'].get('Screen size')
        return data['productFeatures'].apply(lambda x: x.get('Screen size'))

    def __generateProductStorageCapacityFromProductFeatures(self, data: pd.DataFrame):
        # return data['productFeatures'].get('Memory storage capacity')
        return data['productFeatures'].apply(lambda x: x.get('Memory storage capacity'))

    def __generateProductColorFromProductFeatures(self, data: pd.DataFrame):
        return data['productFeatures'].apply(
            lambda x: x.get('Colour'))
        # return data['productFeatures'].get('Colour')

    def __generateProductModelFromProductFeatures(self, data: pd.DataFrame):
        # return data['productFeatures'].get('Model name')
        #
        return data['productFeatures'].apply(
        lambda x: x.get('Model name'))

    def __getProductDeliveryFee(self,data: pd.DataFrame):
        postage_pattern = r"\d+\.\d{2}"
        return  data['productLocation'].apply(lambda x: self.extract_delivery_fee(x,postage_pattern))

    def extract_delivery_fee(self,product_location, pattern):
        if isinstance(product_location, str):
            match = re.search(pattern, product_location)
            return match.group(1) if match else 0
        return 0

    # def __getDeliveryFeeInEuros(self,data):
    #     return  data.apply(self.extractDeliveryFeesInEuros)
    #
    # def extractDeliveryFeesInEuros(self, info):
    #     pattern = r"(?:EUR\s*([0-9]+(?:\.[0-9]{1,2})?)|Free)"
    #     match = re.search(pattern, info)
    #     if match:
    #         return match.group(1) if match.group(1) else 0
    #     return None

    # def __getProductLocation(self,data: pd.DataFrame):
    #     located_in_pattern = r"Located in:\s*(.+)"
    #     return  data['productLocation'].apply(lambda x: re.search(located_in_pattern, x).group(1) if isinstance(x, str) else None)

    def __getEarliestDeliveryDate(self,data: pd.DataFrame):
        date_pattern = r"\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s\d{1,2}\s(?:January|Febuary|March|April|May|June|July|August|September|October|November|December)\b"

        return data['deliveryDetails'].apply(lambda x: re.search(date_pattern, x).group(0) if re.search(date_pattern, x) else None)

    def __getProductsWithFreeDelivery(self,data: pd.DataFrame):
        return data['deliveryFee'] == 0


    def __standardisePrroductRatingOver5(self,data: pd.DataFrame):
        ratingInPercentage=self.__extractRatingInPercentage(data)
        if ratingInPercentage is None:
            return None
        ratingInPercentage=ratingInPercentage.str.replace("%","").astype(float)
        return ratingInPercentage/20

    def __extractRatingInPercentage(self,data: pd.DataFrame):
        percentagePattern= r"\d{1,2}.\d?%"
        return data['productRating'].apply(lambda x: re.search(percentagePattern, x).group(0) if re.search(percentagePattern, x) else None)



    def test(self):
        df= pd.read_csv("/Users/odekunleolasubomi/PycharmProjects/PriceGuard/ab.csv")
        df=df[df["productStore"]=="AMAZON"]
        self.transformData(df)


if __name__ == "__main__":
        a= AmazonTransformer()
        a.test()


