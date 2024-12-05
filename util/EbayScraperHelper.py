# from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
#
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from dotenv import load_dotenv
# import re;
# from math import ceil
# import multiprocessing
# import os
# import pickle
#
# class EbayScraperHelper:
#     ebayScraperInstance = None
#     @staticmethod
#     def createANewSeleniumDriver():
#         service = Service(executable_path=os.getenv("EXE_PATH"))
#         driver = webdriver.Chrome(service=service)
#         return driver
#
#     @staticmethod
#     def executeGetProductDetailsWithAProcess(seralizedProductList):
#         productList = pickle.loads(seralizedProductList)
#         driver=EbayScraperHelper.createANewSeleniumDriver()
#         for product in productList.values():
#             EbayScraperHelper.ebayScraperInstance._getDetailedInformationAboutProduct(product)
#     @staticmethod
#     def getDetailedInformationAboutProductWhileUtilisingParallelism(ebayScraper, productList:dict):
#         EbayScraperHelper.ebayScraperInstance = ebayScraper
#         numberOfCores = int(os.getenv("NUMBER_OF_CORES",1))
#
#         chunksList=EbayScraperHelper.splitProductListIntoChunks(productList);
#         processList=[]
#         processResultList=[]
#         # processResultDic={}
#         # multiprocessing.set_start_method('fork')
#         futuresList=[]
#
#
#         # driver=
#         # process = multiprocessing.Process(target=EbayScraperHelper.executeGetProductDetailsWithAProcess, args=(chunks,driver))
#         # processList.append(process)
#         # with multiprocessing.Pool(numberOfCores) as pool:
#         #     pool.map(EbayScraperHelper.executeGetProductDetailsWithAProcess,(chunks,driver))
#         multiprocessing.set_start_method('fork')
#         with ProcessPoolExecutor(max_workers=2) as executor:
#
#             for chunks in chunksList:
#                 serializedChunks = pickle.dumps(chunks)
#                 futuresList.append(executor.submit(EbayScraperHelper.executeGetProductDetailsWithAProcess, serializedChunks))
#
#             for future in as_completed(futuresList):
#                 future.result()
#         # for process in processList:
#         #     process.start()
#         #
#         # for process in processList:
#         #     processResultList.append(process.join())
#
#         # for processResult in processResultList:
#         #     processResultDic.update(processResult)
#         # return processResultDic
#
#     @staticmethod
#     def splitProductListIntoChunks(productList:dict):
#         numberOfCores = int(os.getenv("NUMBER_OF_CORES",1))
#         chunkSize=ceil(len(productList)/numberOfCores)
#         chunkList=[]
#         chunkDictionary={}
#         for i,(key,value) in enumerate(productList.items()):
#             chunkDictionary[key]=value
#             if (i+1)%chunkSize ==0 or i+1 == len(productList):
#                 chunkList.append(chunkDictionary)
#                 chunkDictionary={}
#         return chunkList
#
# if __name__ == '__main__':
#     pass
# #     EbayScraperHelper.executeGetProductDetailsWithAProcess()
#
