from PriceGuard import PriceGuard
import pandas as pd

p=PriceGuard("IE","Iphone 16","EUR")
scrapedData1=p.performDataAcquisition()
p.performDataTransformation(pd.read_csv(scrapedData1))


