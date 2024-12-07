import unittest

from PriceGuard import PriceGuard
from db.PostgreSql import PostgreSql
import pandas as pd


class PriceGuardUnit(unittest.TestCase):
    postgresSql = PostgreSql(mode="test")
    productName="Iphone 16"
    currency="EUR"
    countryCode="IE"

    priceGuard= PriceGuard(countryCode,productName,currency,postgresSql)

    def tearDown(self):
        self.postgresSql.dropTable(self.productName)
    def test_prepare_data(self):
        dataFrameFromPreparedData=self.priceGuard.prepareData()
        dataFrameFromValueInsertedIntoDataBase= self.postgresSql.retrieveTableAsDataFrame(self.productName)
        assert dataFrameFromPreparedData.equals(dataFrameFromValueInsertedIntoDataBase)

    def test_prepare_data_confirm_product_price_column_is_type_float(self):
        dataFrameFromPreparedData=self.priceGuard.prepareData()
        self.assertTrue(dataFrameFromPreparedData["productPrice"].dtype=="float64")
        # pd.DataFrame(dataFrameFromPreparedData).dtypes
