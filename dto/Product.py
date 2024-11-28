from datetime import datetime
import json
class Product:
    def __init__(self,productStore):
        self.__productLink=""
        self.__productName=""
        self.__productDescription=""
        self.__productPrice=""
        self.__productImage=""
        self.__productFeatures={}
        self.__productRating=0
        self.__maxProductRating=5
        self.__deliveryFee=0
        self.__isInStock=False
        self.__productCurrency=""
        self.__deliveryDetails=""
        self.__discountPercentage=""
        self.__priceBeforeDiscount=0
        self.__event=""
        self.__productScrapeDate=datetime.now()
        self.__productStore=productStore
        self.__productCategory=""
        self.__productId=""
        self.__productLocation=""

    def getProductId(self):
        return self.__productId
    
    def setProductId(self,productId):
        self.__productId=productId

    def getProductLink(self):
        return self.__productLink;

    def setProductLink(self,productLink):
        self.__productLink=productLink
    
    def getProductName(self):
        return self.__productName
    
    def setProductName(self,productName):
        self.__productName=productName

    def getProductImage(self):
        return self.__productImage
    
    def setProductImage(self,productImage):
        self.__productImage=productImage
    
    def getProductDescription(self):
        return self.__productDescription
    def setProductDescription(self,productDescription):
        self.__productDescription=productDescription
    def getProductPrice(self):
        return self.__productPrice
    def setProductPrice(self,productPrice):
        self.__productPrice=productPrice
    def getProductFeature(self):
        return self.__productFeatures
    
    def setProductFeatures(self,productFeatures):
        self.__productFeatures=productFeatures

    def getProductRating(self):
        return self.__productRating
    
    def setProductRating(self,productRating):
        self.__productRating=productRating

    def getMaxProductRating(self):
        return self.__maxProductRating

    def setMaxProductRatng(self,maxProductRating):
        self.__maxProductRating=maxProductRating

    def getDeliveryFee(self):
        return self.__deliveryFee
    
    def setDeliveryFee(self,deliveryFee):
        self.__deliveryFee=deliveryFee
    
    def getIsInStock(self):
        return self.__isInStock;

    def setIsInStock(self,isInStock):
        self.__isInStock=isInStock

    def getProductCurrency(self):
        return self.__productCurrency
    
    def setProductCurrency(self,productCurrency):
        self.__productCurrency=productCurrency

    def getDeliveryDetails(self):
        return self.__deliveryDetails
    
    def setDeliveryDetails(self,deliveryDetails):
        self.__deliveryDetails=deliveryDetails
    
    def getDiscountPercentage(self):
        return self.__discountPercentage

    def setDiscountPercentage(self,discountPercentage):
        self.__discountPercentage=discountPercentage

    def getPriceBeforeDiscount(self):
        return self.__priceBeforeDiscount

    def setPriceBeforeDiscount(self,priceBeforeDiscount):
        self.__priceBeforeDiscount= priceBeforeDiscount

    def getEvent(self):
        return self.__event

    def setEvent(self,event):
        self.__event= event


    def getProductScrapeDate(self):
        return self.__productScrapeDate
    
    def setProductScrapeDate(self,productScrapeDate):
        self.__productScrapeDate=productScrapeDate

    def getProductStore(self):
        return self.__productStore
    def setProductStore(self,productStore):
        self.__productStore=productStore

    def getProductCategory(self):
        return self.__productCategory

    def setProductCategory(self,productCategory):
        self.__productCategory=productCategory

    def getProductLocation(self):
        return self.__productLocation

    def setProductLocation(self,productLocation):
        self.__productLocation=productLocation

    def to_dict(self):
        return {
            "productLink": self.__productLink,
            "productName": self.__productName,
            "productDescription": self.__productDescription,
            "productPrice": self.__productPrice,
            "productImage": self.__productImage,
            "productFeatures": self.__productFeatures,
            "productRating": self.__productRating,
            "maxProductRating": self.__maxProductRating,
            "deliveryFee": self.__deliveryFee,
            "isInStock": self.__isInStock,
            "productCurrency": self.__productCurrency,
            "deliveryDetails": self.__deliveryDetails,
            "discountPercentage": self.__discountPercentage,
            "priceBeforeDiscount": self.__priceBeforeDiscount,
            "event": self.__event,
            "productScrapeDate": self.__productScrapeDate.isoformat(),
            "productStore": self.__productStore,
            "productCategory": self.__productCategory,
            "productId": self.__productId,
            "productLocation": self.__productLocation
        }

    # def __str__(self):
    #     return self.to_dict()


