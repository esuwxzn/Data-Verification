#!/usr/bin/python
#coding: UTF-8

class sqlDatabaseConf:

    def __init__(self):
        
        #Mysql login information
        self.host = 'localhost'
        self.username = 'root'
        self.password = 'root'

#Transaction database
class transaction:
    def __init__(self):

        self.transactionDatabase = 'CUSTOMER'
        self.inwardTable = 'inward_201707'
        self.outwardTable = 'outward_201707'


#Exchange rate database
class exchangeRate:
    def __init__(self):

        self.exchangeRateDatabase = 'CUSTOMER'
        self.exchangeRateTable = 'fx_rate_2017'


#Account number to CIF

class invm:
    def __init__(self):

        self.invmDatabase = 'CUSTOMER'
        self.invmTable = 'invm'



#Customer information
class customerInfo:
    def __init__(self):

        self.customerInfoDatabase = 'CUSTOMER'
        self.customerInfoTable = 'cus'

#Database list
class databaseList:

    def __init__(self):
       self.transaction = transaction()
       self.exchangeRate = exchangeRate()
       self.customerInfo = customerInfo()
       self.invm = invm()

