from transformer.EbayPhonesTransformer import EbayPhonesTransformer


class EbayTransformerFactory:
    def __init__(self):
        pass

    def createTransformer(self, name:str):
        if("phone" in name.lower()):
            return  EbayPhonesTransformer();