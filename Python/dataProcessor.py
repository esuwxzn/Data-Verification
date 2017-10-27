#!/usr/bin/python
#coding: UTF-8

from dataClasses import taxStatisticData, processedTransactionData
from sqlOperation import sqlOperation
from sqlDatabaseConf import databaseList

class dataProcessor:

    def __init__(self, inputData):
        self.inputData = inputData
        self.processedData = processedTransactionData()
        self.database = databaseList()



    def generateQuerySQL(self, **queryInfo):
        

        queryType = queryInfo[queryType]


        if queryType == 'EXCHANGERATE'
            
            currency = queryInfo[currency]
            date = queryInfo[data]
            table = self.database.exchangeRateTable
            return 'SELECT %s FROM %s WHERE DATE = %s' % (currency, table, date)
       
       elif queryType == 'TAXCODE'

            currency = queryInfo[currency]
            date = queryInfo[data]
            table = self.database.exchangeRateTable
            return 'SELECT %s FROM %s WHERE DATE = %s' % (currency, table, date)


    def retriveExchangeRate(self, cur, date):

        SQL = sqlOperation()

        sql = self.generateQuerySQL(cur, date, '')
        
        #print sql
        
        SQL.run(self.database.exchangeRateDatabase, sql) 
       

        return SQL.data[0][0]

     
    def retriveTaxCode(self, CIF):

        SQL = sqlOperation()

        sql = self.generateQuerySQL('', '', CIF)
        
        #print sql
        
        SQL.run(self.database., sql) 
       

        return SQL.data[0][0]


    def convertCurToSEK(self, valueDate, currency, fx_rate_index, SEK_index, row):
        
        fx_rate = self.retriveExchangeRate(currency, valueDate)
        
        originalList = list(row)
        originalList.insert(fx_rate_index, fx_rate)
        originalList.insert(SEK_index, float(originalList[3]) * fx_rate)
        print originalList
        return tuple(originalList)



    def insertToOutputData(self, outputData, key, value):
        if not outputData.has_key(key):    
            outputData[key] = [value,]
        else:   
            outputData[key].append(value)
    


    def distributeTransaction(self, Type):


        for row in self.inputData.inwardData:

            if Type == 'INWARD':
                
                valueDate    = row[0]
                currency     = row[4]
                cif_read     = row[5]
                from_country = row[2]
                fx_rate_index = 6
                SEK_index = 7

            elif Type == 'OUTWARD':

                valueDate    = row[0]
                currency     = row[4]
                cif_read     = row[6]
                to_country   = row[2]
                fx_rate_index = 8
                SEK_index = 9
                tax_code = retrieveTaxFlag(cif_read)

            updatedRow = self.convertCurToSEK(valueDate, currency, fx_rate_index, SEK_index, row)

            if Type == 'INWARD':
                if cif_read != '' and from_country != 'SE' and from_country != '00':
                    self.insertToOutputData(self.processedData.inwardData.dataToReport, cif_read, updatedRow)
                
                else:
                    self.insertToOutputData(self.processedData.inwardData.dataToManual, cif_read, updatedRow)
            elif Type == 'OUTWARD':

                if cif_read != '' and to_country != 'SE' and from_country != '00':
                    self.insertToOutputData(self.processedData.inwardData.dataToReport, cif_read, updatedRow)
                
                else:
                    self.insertToOutputData(self.processedData.inwardData.dataToManual, cif_read, updatedRow)
                
    
    
    def run(self):
        
        self.distributeTransaction('INWARD')
        return self.processedData
