# encoding=utf-8
# this project is powered by Jeff Omega
# as author is a newbie to python, code style of this project is rubyish
# as a convention, class name is capitalized and instance is lower-cased
# and this project is migrated from btc38_1 project which is forked from
# a btc38 gem from github


import error_code
import json
import error
import time

class OrderInfo:
    def __init__(self, currency_pair, result, params):
        try:
            result=json.loads(result)
            self.order_id=""
            if result["result"]==True:
                self.order_id=result["order_id"]
                self.price=params["price"]
                self.amount=params["amount"]
                self.type=params["type"]
                self.message="操作成功"
            else:
                self.message=error_code.Error_code_for_OKEx[result["error_code"]]
        except:
            self.order_ids=[]
            self.message="Unknow error"

#  this class represents the orders that you HAVE already submitted,
# NOT the orders you are submitting!!!
class SubmittedOrderList:
    def __init__(self,currency_pair,result):
        result=json.loads(result)
        if result.__contains__("result") and result["result"]==True:
            if result.__contains__("total"):
                self.orders=[]
                self.total=result["total"]
                orders=result["orders"]
                for order in orders:
                    currency_pair=order["symbol"]
                    id=int(order["order_id"])
                    price=float(order["price"])
                    total_amount=float(order["amount"])
                    trade_amount=float(order["deal_amount"])
                    status=int(order["status"])
                    trade_price=float(order["avg_price"])
                    trade_money=trade_amount*trade_price
                    trade_type=(1 if order["type"]=="buy" else 0)
                    this_order=SubmittedOrder(currency_pair,id,price,status,total_amount,trade_amount,trade_money,trade_price,trade_type)
                    self.orders.append(this_order)
                    self.message="操作成功"
        else:
            self.message=error_code.Error_code_for_OKEx[result["error_code"]]

class SubmittedOrder:
    def __init__(self, currency_pair, id, price, status, total_amount,
                 trade_amount,  trade_money, trade_price, trade_type):
        self.currency_pair=currency_pair
        self.id=id
        self.price=price
        self.status=status
        self.total_amount =total_amount
        self.trade_amount=trade_amount
        self.trade_money=trade_money
        self.trade_price=trade_price
        self.trade_type=trade_type

class CancelOrderResult:
    def __init__(self, market, currency_pair, result, order_id):
        self.currency_pair=currency_pair
        result=json.loads(result)
        market=str(market).lower()
        if market=="chbtc":
            pass
        elif market=="okex":
            if result.__contains__("result"):
                self.result=True
                self.message="操作成功"
                self.id=order_id
            else:
                self.result=False
                self.message=error_code.Error_code_for_OKEx[result["error_code"]]
                self.id=order_id

class Order:
    def __init__(self,price , amount):
        self.price=price
        self.amount=amount


class Bid(Order):
    pass

class Ask(Order):
    pass


class Depth(object):
    def __init__(self, market, currency_pair, result):
        '''
        the Depth class instance has the following data members:
        bids:  Array of Bid
        asks:  Array of Ask
        timestamp:  Long
        message:  String
        market:  String
        currency_pair:  String
        :param market:  represents which market you are in
        :param currency_pair: represents which currency pair you are trading with
        :param result: represents the json that the server returns to you
        '''
        self.bids=[]
        self.asks=[]
        self.timestamp=int(time.time())
        self.market=market
        self.currency_pair=currency_pair
        self.message="True"
        try:
            market=str(market).lower()
            # result=json.loads(str(result))
            if market=="okex":
                if dict(result).__contains__("asks"):
                    bss=result['bids']  # the bids object in the json
                    ass=result['asks']  # the asks object in the json
                    for b in bss:
                        bid=Bid(b[0],b[1])
                        self.bids.append(bid)
                    for a in ass:
                        ask=Ask(a[0],a[1])
                        self.asks.append(ask)
                    self.asks.reverse()
                elif dict(result).__contains__("error_code"):
                    self.message=error_code.Error_code_for_OKEx[result["error_code"]]
            elif market=="chbtc":
                pass
            elif market=="btc38":
                pass
        except Exception as e:
            self.message=e
        finally:
            pass

    def __sub__(self, other):
        import copy
        result=copy.deepcopy(self)
        size_of_bids=len(result.bids)
        size_of_asks=len(result.asks)
        if other.__class__ is Depth:
            for bid in other.bids:
                price=bid.price
                amount=bid.amount
                cnt=0
                while cnt<size_of_bids:
                    if result.bids[cnt].price==price:
                        result.bids[cnt].amount-=amount
                    cnt+=1

            for ask in other.asks:
                price=ask.price
                amount=ask.amount
                cnt=0
                while cnt<size_of_asks:
                    if result.asks[cnt].price==price:
                        result.asks[cnt].amount-=amount
                    cnt+=1
        else:
            pass

    def mid_point(self, weighted_by=None, distance=1):
        if weighted_by==None:
            bid_price=self.bids[distance-1].price
            ask_price=self.asks[distance-1].price
            return (bid_price+ask_price)/2.0

    '''
    here distance means accumulated amount, e.g:
    bid0: 0.1
    bid1: 0.05
    bid2: 0.11
    bid3: 0.07
    here, if the distance is 0.2, 
    bid0+bid1+bid2 is just beyond the distance, then
    the price of bid3 is the target price
    
    but when you think about it, you dont really need this function,
    because before long, you would use tensorflow as the backend to
    calculate and deduce the pattern, then this strategy is useless!
    '''

class Ticker(object):
    # :market, :currency, :timestamp, :high,
    # :low, :last, :vol, :buy, :sell, :message

    def __init__(self, market, currency_pair, result):
        try:
            self.market=market
            self.currency_pair=currency_pair
            if dict(result).__contains__("ticker"):
                ticker=result["ticker"]
                self.buy=float(ticker["buy"])
                self.sell=float(ticker["sell"])
                self.vol=float(ticker["vol"])
                self.high=float(ticker["high"])
                self.low=float(ticker["low"])
                self.last=float(ticker["last"])
                self.timestamp=int(result["date"])
                self.message="操作成功"
            elif dict(result).__contains__("error_code"):
                self.buy=0
                self.sell=0
                self.vol=0
                self.high=0
                self.low=0
                self.last=0
                self.timestamp=0
                error_key=result["error_code"]
                self.message=error_code.Error_code_for_OKEx[error_key]
        except Exception as e:
            self.message=e

class TradeInfo:
    '''
    :timestamp, :price, :amount, :trade_type, :tid
    '''
    def __init__(self,timestamp, price, amount, trade_type, tid, status=-999):
        '''

        :param timestamp:
        :param price:
        :param amount:
        :param trade_type:
        :param tid:
        :param status: -1 for drawn, 0 for pending, 1 for partially traded, 2 for complete, 3 for 撤单处理中
        -999 for unknown
        '''
        self.timestamp = timestamp
        self.amount = amount
        self.price = price
        self.trade_type=trade_type
        self.tid=tid
        self.status=status

class Trades:
    '''
    this class represents a series of trades, whose attribute trades is an array of TradeInfo instances
    this class has 3 data members: :market, :currency, :trades, message
    '''

    def __init__(self,market, currency_pair, result, status):
        self.market=market
        self.currency_pair=currency_pair
        self.trades=[]
        market=str(market).lower()
        try:
            result=list(result)
            if market=="okex":
                for item in result:
                    if item["type"]=="buy":
                        trade_type=1
                    else:
                        trade_type=0
                    trade=TradeInfo(item["date"],item["price"],item["amount"],trade_type,item["tid"],status)
                    self.trades.append(trade)
                self.message="操作成功"
        except Exception as e:
            self.message=e

class BalanceInfo:
    '''
                :timestamp, :market, :total_asset, :net_asset, :free_cny,:free_btc,:frozen_btc,:free_ltc,:free_bcc,:free_eth,:free_etc,:free_bts,:free_hsr,
                :free_eos,:frozen_cny,:frozen_ltc,:frozen_bcc,:frozen_eth,:frozen_etc,:frozen_bts,:frozen_hsr,:frozen_eos,
                :free_usdt, :frozen_usdt, :free_bch, :frozen_bch, :free_btg, :frozen_btg, :free_gas , :frozen_gas, :free_zec , :frozen_zec, :free_neo , :frozen_neo,
                :free_iota , :frozen_iota, :free_gnt , :frozen_gnt, :free_snt , :frozen_snt, :free_dash , :frozen_dash , :free_xuc , :frozen_xuc, :free_qtum , :frozen_qtum,
                :free_omg , :frozen_omg,
                :message
    this is bewildering....
    fuck that....
    BalanceInfo class should have the following data members:
    1. timestamp
    2. market
    3. total_asset
    4. net_asset
    5. free
    6. frozen
    7. message
    '''

    def __init__(self, market, result):
        self.timestamp=time.time()
        self.market=market
        self.free={}
        self.frozen={}
        market=str(market).lower()
        try:
            if market=="okex":
                result=json.loads(result)
                if result["result"]==True:
                    self.message="操作成功"
                    self.free=result["info"]["funds"]["free"]
                    self.free.pop("bcc")
                    self.frozen=result["info"]["funds"]["freezed"]
                    self.frozen.pop("bcc")
                else:
                    self.message=error_code.Error_code_for_OKEx[dict(result)["error_code"]]

        except Exception as e:
            self.message=e
