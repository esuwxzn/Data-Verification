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
        self.transactionDatabase = 'TEST'
        
        self.inwardTable = 'inward'
        self.outwardTable = 'outward'
        
        #Exchange rate database
        self.exchangeRateDatabase = 'EXCHANGERATE'
        
        self.exchangeRateTable = 'exchangerate'
        
        #Customer information
        self.customerInfoDatabase = 'CUSTOMERINFO'

        self.customerInfoTable = 'customerinfo'
