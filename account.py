# -*- coding: UTF-8 -*-
import csv
import universal

def get_key_pair(discription="test"):
    f=open('API_list.csv','r')
    reader=csv.reader(f)
    result=[]
    for row in reader:
        if row[9]==discription:
            result= [row[7],row[8],row[3]]
    f.close()
    return result

class Account:
    def __init__(self, description="test"):
        key_pair=get_key_pair(description)
        self.api_key=key_pair[0]
        self.secret_key=key_pair[1]
        self.description=description
        self.name=key_pair[2]

    def set_balance(self, balance_info):
        self.balance_info=balance_info  # universal.BalanceInfo class

    def set_orders(self, orders):
        self.orders=orders