class CurrencyPair:
    def __init__(self,base='btc', reference='usdt'):
        self.base=base
        self.reference=reference

    def get_currency_pair(self):
        return self.base+'_'+self.reference

    def get_referencial_currencies(self, market):
        market=str(market).lower()
        if market=="okex":
            return ["btc","usdt","eth","bch"]
        elif market=="chbtc" or market=="zb":
            pass
        elif market=="???":
            pass
        else:
            pass

    def get_referencial_currency(self, string):
        try:
            reference=str(string).split("_")[1]
        except Exception as e:
            reference=None
        return reference

    def get_base_currency(self, string):
        try:
            reference=str(string).split("_")[0]
        except Exception as e:
            reference=None
        return reference