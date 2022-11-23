import requests, json
import pandas as pd
from datetime import datetime as dt, timedelta, date
import time
import pytz

class Config:
    def __init__(self, account_type):
        if account_type == 'Live':
            self.acc_type = 'LIVE'
            self.endpoint = 'https://api.ig.com/gateway/deal'
        else:
            self.acc_type = 'DEMO'
            self.endpoint = 'https://demo-api.ig.com/gateway/deal'
            
class IG:
    def __init__(self, key, username, password, account, acc_type='DEMO'):
        self.api_key = key
        self.username = username
        self.password = password
        self.account_type = acc_type
        self.account_num = ''
        self.CST = ''
        self.X_SECURITY_TOKEN = ''
        self.lightstreamerEndpoint = ''
        self.s = requests.Session()
        self.config = Config(self.account_type)
        self.ls_client = None
        self.version = '1.0.2'
        
    def getVersion(self):
        return self.version
    
    def login(self):
        response = self.s.post(self.config.endpoint+'/session', headers={'X-IG-API-KEY': self.api_key, 'Content-Type': 'application/json; charset=UTF-8', 'Accept': 'application/json; charset=UTF-8', 'VERSION': '2'}, data=json.dumps({"identifier":self.username, "password":self.password}))
        self.CST = response.headers['CST']
        self.X_SECURITY_TOKEN = response.headers['X-SECURITY-TOKEN']
        
        
    def account(self):
        response = self.s.get(self.config.endpoint+'/accounts', headers={'X-IG-API-KEY': self.api_key, 'CST': self.CST, 'X-SECURITY-TOKEN': self.X_SECURITY_TOKEN, 'Content-Type': 'application/json;', 'Accept': 'application/json; charset=UTF-8', 'VERSION': '1'})
        time.sleep(0.5)
        data = json.loads(response.text)
        df = pd.DataFrame.from_dict(data['accounts'])
        df = df.set_index('accountId')
        return df
    
    def getAccountTransactions(self):
        response = self.s.get(self.config.endpoint+'/history/transactions', headers={'X-IG-API-KEY': self.api_key, 'CST': self.CST, 'X-SECURITY-TOKEN': self.X_SECURITY_TOKEN, 'Content-Type': 'application/json;', 'Accept': 'application/json; charset=UTF-8', 'VERSION': '2'}, data={'pageSize': 0})
        time.sleep(0.5)
        data = json.loads(response.text)
        df = pd.DataFrame(data['transactions'])
        return df
    
    def getAccountActivities(self):
        response = self.s.get(self.config.endpoint+'/history/activity', headers={'X-IG-API-KEY': self.api_key, 'CST': self.CST, 'X-SECURITY-TOKEN': self.X_SECURITY_TOKEN, 'Content-Type': 'application/json;', 'Accept': 'application/json; charset=UTF-8', 'VERSION': '2'}, data={'pageSize': 0})
        time.sleep(0.5)
        data = json.loads(response.text)
        df = pd.DataFrame(data['activities'])
        return df
    
    def getBalance(self, account_num=''):
        acc = self.account()
        if account_num == '':
            account_num = self.account_num
        return acc.loc[account_num, 'balance']['balance']
    
    def getAvailable(self, account_num=''):
        acc = self.account()
        if account_num == '':
            account_num = self.account_num
        return acc.loc[account_num, 'balance']['available']
    
    def getDeposit(self, account_num=''):
        acc = self.account()
        if account_num == '':
            account_num = self.account_num
        return acc.loc[account_num, 'balance']['deposit']
    
    def getProfitLoss(self, account_num=''):
        acc = self.account()
        if account_num == '':
            account_num = self.account_num
        return acc.loc[account_num, 'balance']['profitLoss']
    
    def watchlists(self):
        response = self.s.get(self.config.endpoint+'/watchlists', headers={'X-IG-API-KEY': self.api_key, 'CST': self.CST, 'X-SECURITY-TOKEN': self.X_SECURITY_TOKEN, 'Content-Type': 'application/json;', 'Accept': 'application/json; charset=UTF-8', 'VERSION': '1'})
        time.sleep(0.5)
        data = json.loads(response.text)
        df = pd.DataFrame(data['watchlists'])
        df = df.set_index('name')
        return df
    
    def watchlist(self, id):
        response = self.s.get(self.config.endpoint+'/watchlists/'+id, headers={'X-IG-API-KEY': self.api_key, 'CST': self.CST, 'X-SECURITY-TOKEN': self.X_SECURITY_TOKEN, 'Content-Type': 'application/json;', 'Accept': 'application/json; charset=UTF-8', 'VERSION': '1'})
        time.sleep(0.5)
        data = json.loads(response.text)
        df = pd.DataFrame(data['markets'])
        df = df.set_index('epic')
        return df
    
    def getPrice(self, epic, resolution='', numPoints=0):
        response = self.s.get(self.config.endpoint+'/markets/'+epic, headers={'X-IG-API-KEY': self.api_key, 'CST': self.CST, 'X-SECURITY-TOKEN': self.X_SECURITY_TOKEN, 'Content-Type': 'application/json;', 'Accept': 'application/json; charset=UTF-8', 'VERSION': '2'})
        time.sleep(0.5)
        data = json.loads(response.text)
        tz = pytz.timezone('Europe/London')
        d = dt.now(tz).strftime("%Y-%m-%d")
        df = pd.DataFrame([data['snapshot']])
        df['updateTime'] = d+' '+df['updateTime']
        return df

    def getPrices(self, epic, resolution='', numPoints=0, start='', end=''):
        params = epic
        if resolution != '' and numPoints != 0:
            params += '/'+resolution+'/'+str(numPoints)
        elif resolution != '' and start != '' and end != '':
            params += '/'+resolution+'/'+start+'/'+end
        response = self.s.get(self.config.endpoint+'/prices/'+params, headers={'X-IG-API-KEY': self.api_key, 'CST': self.CST, 'X-SECURITY-TOKEN': self.X_SECURITY_TOKEN, 'Content-Type': 'application/json;', 'Accept': 'application/json; charset=UTF-8', 'VERSION': '2'})
        data = json.loads(response.text)
        df = pd.DataFrame(data['prices'])
        return df
    
    def getOpenPosition(self, dealId=''):
        params = ''
        if dealId != '':
            params = '/'+str(dealId)
        response = self.s.get(self.config.endpoint+'/positions'+params, headers={'X-IG-API-KEY': self.api_key, 'CST': self.CST, 'X-SECURITY-TOKEN': self.X_SECURITY_TOKEN, 'Content-Type': 'application/json;', 'Accept': 'application/json; charset=UTF-8', 'VERSION': '2'})
        time.sleep(0.5)
        data = json.loads(response.text)
        if dealId != '': 
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame(data['positions'])
        return df
    
    def closePosition(self, dealId, direction, expiry, orderType, size):
        response = self.s.post(self.config.endpoint+'/positions/otc', headers={'X-IG-API-KEY': self.api_key, 'CST': self.CST, 'X-SECURITY-TOKEN': self.X_SECURITY_TOKEN, 'Content-Type': 'application/json;', 'Accept': 'application/json; charset=UTF-8', '_method':'DELETE', 'VERSION': '1'}, data=json.dumps({"dealId": dealId, "direction": direction, "expiry": expiry, "orderType": orderType, "size": size}))
        time.sleep(0.5)
        data = json.loads(response.text)
        return data['dealReference']
    
    def createPosition(self, currency, direction, epic, expiry, orderType, size, limitDistance=None, stopDistance=None, forceOpen=True, guaranteedStop=False):
        response = self.s.post(self.config.endpoint+'/positions/otc', headers={'X-IG-API-KEY': self.api_key, 'CST': self.CST, 'X-SECURITY-TOKEN': self.X_SECURITY_TOKEN, 'Content-Type': 'application/json;', 'Accept': 'application/json; charset=UTF-8', 'VERSION': '2'}, data=json.dumps({"currencyCode": currency, "direction": direction, "epic": epic, "expiry": expiry, "orderType": orderType, "size": size, "limitDistance": limitDistance, "stopDistance": stopDistance, "forceOpen": forceOpen, "guaranteedStop": guaranteedStop}))
        time.sleep(0.5)
        data = json.loads(response.text)
        return data['dealReference']
