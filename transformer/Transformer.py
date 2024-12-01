from abc import ABC, abstractmethod
import pandas as pd

class Transformer(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def transformData(self,data:pd.DataFrame):
        "Perform data transformation"
        pass
