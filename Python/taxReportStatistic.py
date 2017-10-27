#!/usr/bin/pythssedTransactionData
#coding: UTF-8
from dataClasses import taxStatisticData, processedTransactionData


from sqlOperation import sqlOperation
from fileGenerator import fileGenerator
from dataProcessor import dataProcessor

from sqlDatabaseConf import databaseList


class taxReportStatistic:

    def __init__(self):
        #self.fileGenerator = fileGenerator()

        self.data = taxStatisticData()
        self.processedTransData = processedTransactionData()
        self.database = databaseList()

    def generateQuerySQL(self, table, queryType):

        if queryType == 'INWARD':

            return "SELECT DP03_VALU_DATE, CP03_EXTN_REF_NO, FROM_CON, CP03_PAY_AMT, CP03_PAY_CURR, CP03_BEN_CUS_NO FROM %s" % self.database.inwardTable

        elif queryType == 'OUTWARD':

            return "SELECT DP04_VALU_DATE, CP04_EXTN_REF_NO, TO_CON, CP04_PAY_AMT, CP04_PAY_CURR FROM %s" % self.database.outwardTable



    def queryData(self, queryType):
        
        database = ''
        sql = ''

        SQL = sqlOperation()

        if queryType == 'INWARD' or queryType == 'OUTWARD':
            
            database = self.database.transactionDatabase
            sql = self.generateQuerySQL('', queryType)
        
        elif queryType == 'EXCHANGERATE':
            database = self.database.exchangeRateDatabase
            sql = generateQuerySQL(self.database.exchangeRateTable, queryType)
        
        elif queryType == 'ACCOUNTINFO':
            database = self.database.exchangeRateDatabase
            sql = generateQuerySQL(self.database.customerInfoTable, queryType)
        
        elif queryType == 'ACCOUNTINFO':
            print "Query type is %s" % queryType

        else:
            print "ERROR:Unsupported query type..."
            exit(0)
        
        SQL.run(database, sql)

        return SQL.data


    def retrieveData(self):
        
        self.data.inwardData = self.queryData('INWARD')
        self.data.outwardData = self.queryData('OUTWARD')
#        self.data.exchangeRateData = self.queryData('EXCHANGEREATE')
#        self.data.accountInfoData = self.queryData('ACCOUNTINFO') 
        #self.customerInfoData = self.queryData('CUSTOMERINFO')


    def processData(self, data):
        
        dp = dataProcessor(data)
        self.processedTransData = dp.run()


    def writeDataToFile(self, data):

        fg = fileGenerator(data)
        fg.run()

    def run(self, startTime, endTime):#Start time and end time is not handled here.

        self.retrieveData()
        self.processData(self.data)
        self.writeDataToFile(self.processedTransData)

a = taxReportStatistic()
a.run(1,2)
