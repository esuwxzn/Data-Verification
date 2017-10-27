#!/usr/bin/python
#coding: UTF-8

class sqlDatabaseConf:

    def __init__(self):
        
        #Mysql login information
        self.host = 'localhost'
        self.username = 'root'
        self.password = 'root'


class databaseList:

    def __init__(self):
        #Transaction database
        self.transactionDatabase = 'CUSTOMER'
        
        self.inwardTable = 'inward'
        self.outwardTable = 'outward'
        
        #Exchange rate database
        self.exchangeRateDatabase = 'CUSTOMER'
        
        self.exchangeRateTable = 'fx_rate_2017'
        
        #Customer information
        self.customerInfoDatabase = 'CUSTOMERINFO'

        self.customerInfoTable = 'customerinfo'
