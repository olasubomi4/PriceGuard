# from PriceGuard import PriceGuard
# import pandas as pd
#
# class PriceMain:
#     def prepareData(self,countryCode,productName,currency):
#         p=PriceGuard(countryCode,productName,currency)
#         scrapedData1=p.performDataAcquisition()
#         newCopy=scrapedData1.copy()
#         a=p.performDataTransformation(newCopy)
#         return p.performDataLoading(a)
#     # p.performDataTransformation(pd.read_csv("/Users/odekunleolasubomi/PycharmProjects/PriceGuard/rawData.csv"))
#
#
# if __name__=="__main__":
#     PriceMain().prepareData("IE","Iphone 16","EUR")
#
