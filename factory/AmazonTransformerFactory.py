from transformer.AmazonTransformer import AmazonTransformer


class AmazonTransformerFactory:
    def __init__(self):
        pass

    def createTransformer(self, name:str):
        if("phone" in name.lower()):
            return  AmazonTransformer();