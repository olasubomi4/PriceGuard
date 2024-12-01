from PriceGuard import PriceGuard
import pandas as pd

p=PriceGuard("IE","Iphone 16","EUR")
scrapedData1=p.performDataAcquisition()
newCopy=scrapedData1.copy()
p.performDataTransformation(newCopy)
# p.performDataTransformation(pd.read_csv("/Users/odekunleolasubomi/PycharmProjects/PriceGuard/rawData.csv"))



