from abc import ABC, abstractmethod


class Scraper(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def Scrape(self):
        "Perform web scraping"
        pass
