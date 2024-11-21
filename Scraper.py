from abc import ABC, abstractmethod

class Scraper(ABC):
    @abstractmethod
    def Scrape():
        "Perform web scraping"
        pass



