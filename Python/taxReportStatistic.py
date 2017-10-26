#!/usr/bin/python

#coding: UTF-8

from SQL_Operation import SQL_Operation

from File_Generator import File_Generator

from Data_Processor import Data_Processor

transactionDatabase = 'CUSTOMER'
inwardTable = 'inward'
outwardTable = 'outward'

exchangeRateDatabase = 'EXCHANGERATE'
exchangeRateTable = 'exchangerate'

inwardHeader = ['Transaction Value Date(663)', 'Ref. NO.', 'From(662)', 'AMOUNT', 'Currency(664)', 'Customer', 'Rate', 'SEK', 'Origanisation Number/ID', 'Personal Number', 'Address', 'Tax Code']

outwardHeader = ['Transaction Value Date(663)', 'Ref. NO.', 'To(662)', 'AMOUNT(660)', 'Currency(664)', 'Reasons(661)', 'Customer(671)', 'Beneficiary', 'SEK', 'Origanisation Number/ID', 'Personal Number', 'Address', 'Tax Code']

class taxReportStatistic:

    def __init__(self, date):
        self.SQL = SQL_Operation()
        self.dataProcessor = Data_Processor()
        self.fileGenerator = File_Generator()
        
        self.inwardTransactionData = ''
        self.outwardTransactionData = ''
        self.exchangeRateData = ''
        self.customerInfoData = ''
        self.accountInfoData = ''


    def generateQuerySQL(self, table, queryType):

        if queryType == 'INWARD':

            return "SELECT DP03_VALU_DATE, CP03_EXTN_REF_NO, FROM_CON, CP03_PAY_AMT, CP03_PAY_CURR, CP03_BEN_CUS_NO FROM %s" % inwardTable

        elif queryType == 'OUTWARD':

            return "SELECT DP04_VALU_DATE, CP04_EXTN_REF_NO, TO_CON, CP04_PAY_AMT, CP04_PAY_CURR FROM %s" % outwardTable

   
    def queryData(self, queryType):
        data = ''
        database = ''
        sql = ''

        if queryType == 'INWARD' or queryType == 'OUTWARD':
            
            database = transactionDatabase
            sql = generateQuerySQL(transactionDatabase, queryType)
        
        elif queryType == 'EXCHANGERATE':

            database = exchangeRateDatabase
            sql = generateQuerySQL(exchangeRateDatabase, queryType)

        else:
            print "ERROR:Unsupported query type..."
            exit(0)
        

        self.SQL.run(database, sql)

        return self.SQL.data



    def retrieveData(self):
        
        self.inwardTransactionData = self.queryData('INWARD')
        self.outwardTransactionData = self.queryData('OUTWARD')
        self.exchangeRateData = self.queryData('EXCHANGEREATE')
        #self.customerInfoData = self.queryData('CUSTOMERINFO')
        self.accountInfoData = self.queryData('ACCOUNTINFO') 



    def processData(self):#, processType):
        
        #Covert the currency to SEK. Retrieve the exchange rate first and convert to SEK
        #if processType == 'INWARD':
            
        self.inwardTransactionData = self.dataProcessor.convertToSEK(self.inwardTransactionData, self.exchangeRateData, 'INWARD')

        #elif processType == 'OUTWARD':
        self.outwardTransactionData = self.dataProcessor.convertToSEK(self.outwardTransactionData, self.exchangeRateData, 'OUTWARD')



    def writeDataToFile():


    def run(self, startTime, endTime):#Start time and end time is not handled here.

        self.retrievnData()
        self.processData()
        self.writeDataToFile()


