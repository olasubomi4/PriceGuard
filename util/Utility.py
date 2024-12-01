import ast
import json

class Utility:
    def __init__(self):
        pass


    def convertDictionaryInStringFormatToDictionary(self, stringDictionary):
        try:
            # stringDictionary = stringDictionary.replace('"', " ")
            # stringDictionary = stringDictionary.replace("'", "\"")

            # stringDictionary=stringDictionary.replace("\n", " ")
            return ast.literal_eval(stringDictionary)

        except Exception as e:
            print(e)
            return {}

        # newDictionary = {}
        # stringDictionary=stringDictionary.replace("{", "")
        # stringDictionary=stringDictionary.replace("}", "")
        #
        # key_value_pairs = stringDictionary.split(", ")
        #
        # for pair in key_value_pairs:
        #     # Split each pair into key and value
        #     key, value = pair.split(":")
        #     # Remove any extra whitespace around key and value
        #     key, value = key.strip(), value.strip()
        #     # Add to the new dictionary
        #     newDictionary[key] = value
        #     newDictionary[value] = key  # Reverse mapping
        #
        # return newDictionary

# if __name__ == "__main__":
#     utility = Utility()
#     a=utility.convertDictionaryInStringFormatToDictionary("{'Condition': 'New: A brand-new, unused, unopened and undamaged item in original retail packaging (where packaging ... Read more\nabout the condition', 'Colore': 'Multicolore', 'Capacità di memorizzazione': '256 GB', 'Stile': 'Classico', 'Slot scheda SIM': 'Dual SIM (SIM + eSIM)', 'MPN': 'NON APPLICABILE', 'Garanzia produttore': '2 anni', 'Memoria RAM': '6 GB', 'Processore': 'Hexa Core', 'Tipo di scheda di memoria': 'MicroSD', 'Risoluzione fotocamera': '12,0 MP', 'Contratto': 'Senza contratto', 'Numero modello': '440G', 'Marca': 'Apple', 'Modello': 'Apple iPhone 16', 'Connettività': '5G', 'Dimensioni schermo': '6,1"', 'Stato di blocco': 'Sbloccato da fabbrica', 'Sistema operativo': 'iOS', 'Paese di fabbricazione': 'Italia'}"")
#     print(a)