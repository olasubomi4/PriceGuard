import ast


class Utility:
    def __init__(self):
        pass

    def convertDictionaryInStringFormatToDictionary(self, stringDictionary):
        try:
            stringDictionary = stringDictionary.replace("'", "\"")
            return ast.literal_eval(stringDictionary)

        except :
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

if __name__ == "__main__":
    utility = Utility()
    a=utility.convertDictionaryInStringFormatToDictionary("{'Condition': 'New: A brand-new, unused, unopened and undamaged item in original retail packaging (where packaging ... Read more\\nabout the condition', 'Compatible Brand': 'For Apple', 'Character': 'Max', 'Items Included': 'N/a', 'Custom Bundle': 'Yes', 'Compatible Model': 'For Apple iPhone 11, For Apple iPhone 11 Pro, For Apple iPhone 11 Pro Max, For Apple iPhone 12, For Apple iPhone 12 mini, For Apple iPhone 12 Pro, For Apple iPhone 12 Pro Max, For Apple iPhone 13, For Apple iPhone 13 mini, For Apple iPhone 13 Pro, For Apple iPhone 13 Pro Max, For Apple iPhone 14, For Apple iPhone 14 Plus, For Apple iPhone 14 Pro, For Apple iPhone 14 Pro Max, For Apple iPhone 15, For Apple iPhone 15 Plus, For Apple iPhone 15 Pro, For Apple iPhone 15 Pro Max, For Apple iPhone 7, For Apple iPhone 8, For Apple iPhone SE (2nd Generation), For Apple iPhone SE (3rd Generation), For Apple iPhone X, For Apple iPhone XR, For Apple iPhone XS, For Apple iPhone 16 Pro Max, For Apple iPhone 16 Pro, For Apple iPhone 16, For Apple iPhone 16 Plus', 'MPN': 'Does Not Apply', 'Material': 'Silicone/Gel/Rubber', 'Colour': 'Clear', 'Brand': 'PROMAX', 'Type': 'Soft', 'Version': '4', 'Manufacturer Warranty': '1 Year', 'Design/Finish': 'Glossy, Plain, Transparent', 'Theme': 'N/a', 'Features': '360 Protection, Anti-Scratch, Case Friendly, Lightweight, Non-Slip, Shockproof, Smartcase', 'Country/Region of Manufacture': 'China', 'Wireless Charging Standard': 'Qi', 'Character Family': 'Free!', 'Personalise': 'No'}")
    print(a)