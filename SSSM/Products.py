import math 

class Products:
    def __init__(self, symbol, value, tradeable):
        self.symbol = symbol
        self.value = value
        self.tradeable = tradeable
    
class Shares(Products):
    def __init__(self, symbol, type, value, tradeable, last_dividend, fixed_dividend):
        super().__init__(symbol, value/100.0, tradeable)
        self.type = type
        self.last_dividend = last_dividend/100.0
        self.fixed_dividend = fixed_dividend/100.0 # Percentage

class Index(Products):
    def __init__(self, symbol, composition):
        # Calculate value using geometric mean of prices for all stocks in composition
        self.composition = composition
        super().__init__(symbol, self.__geometric_mean(), False) # Make indices non-tradeable for platform as they're only used for tracking

    def __geometric_mean(self):
        # multiply all n values in prices array together then power to 1/n (nth root)
        prices = list(map(lambda x:x.value, self.composition))
        return round(math.prod(prices)**(1.0/len(prices)) ,5)

