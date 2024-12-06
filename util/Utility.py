import ast
import json
import sys
from datetime import datetime
import pandas as pd

class Utility:
    def __init__(self):
        pass

    @staticmethod
    def predictYearFromDate(dateStr,dateFormat):
        dateValue= datetime.strptime(dateStr,dateFormat)
        currentYear = datetime.now().year
        dataValueWithYear= dateValue.replace(year=currentYear)

        if datetime.now()>dataValueWithYear:
            dataValueWithYear= dataValueWithYear.replace(year=currentYear+1)

        return dataValueWithYear

    @staticmethod
    def convertDictionaryInStringFormatToDictionary(stringDictionary):
        try:
            return ast.literal_eval(stringDictionary)
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def convertStringToFloat(value):
        try:
            return float(value)
        except Exception as e:
            return 0.0

    @staticmethod
    def getDayDifferenceBetweenDates(startDate:pd,endDate:datetime):
        try:
            startDate= pd.to_datetime(startDate)
            endDate=pd.to_datetime(endDate)
            result=abs((endDate -startDate).days)
            return result
        except Exception as e:
            print(e)
            return None

# if __name__ == "__main__":
    # utility = Utility()
    # print(utility.predictYearFromDate("Fri, Dec ","%a, %b %d"))
#     a=utility.convertDictionaryInStringFormatToDictionary("{'Condition': 'New: A brand-new, unused, unopened and undamaged item in original retail packaging (where packaging ... Read more\nabout the condition', 'Colore': 'Multicolore', 'Capacità di memorizzazione': '256 GB', 'Stile': 'Classico', 'Slot scheda SIM': 'Dual SIM (SIM + eSIM)', 'MPN': 'NON APPLICABILE', 'Garanzia produttore': '2 anni', 'Memoria RAM': '6 GB', 'Processore': 'Hexa Core', 'Tipo di scheda di memoria': 'MicroSD', 'Risoluzione fotocamera': '12,0 MP', 'Contratto': 'Senza contratto', 'Numero modello': '440G', 'Marca': 'Apple', 'Modello': 'Apple iPhone 16', 'Connettività': '5G', 'Dimensioni schermo': '6,1"', 'Stato di blocco': 'Sbloccato da fabbrica', 'Sistema operativo': 'iOS', 'Paese di fabbricazione': 'Italia'}"")
#     print(a)