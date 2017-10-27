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

    def generateQuerySQL(self, currency, date):#sitch type 
        
        return 'SELECT %s FROM %s WHERE DATE = %s' % (currency, self.database.exchangeRateTable, date)


    def retriveExchangeRate(self, cur, date):

        SQL = sqlOperation()

        sql = self.generateQuerySQL(cur, date)
        
        #print sql
        
        SQL.run(self.database.exchangeRateDatabase, sql) 
        
        return SQL.data[0][0]

     

    def convertCurToSEK(self, valueDate, currency, row):

        
        fx_rate = self.retriveExchangeRate(currency, valueDate)
        
        originalList = list(row)
        originalList.insert(6, fx_rate)
        originalList.insert(7, float(originalList[3]) * fx_rate)
        print originalList
        return tuple(originalList)


    def insertToOutputData(self, outputData, key, value):
        if not outputData.has_key(key):    
            outputData[key] = [value,]
        else:   
            outputData[key].append(value)

    def distributeTransaction(self):

        for row in self.inputData.inwardData:
       
            valueDate = row[0]
            currency = row[4]
            cif_read = row[5]
            from_country = row[2]

            updatedRow = self.convertCurToSEK(valueDate, currency, row)


            if cif_read != '' and from_country != 'SE' and from_country != '00':
                self.insertToOutputData(self.processedData.inwardData.dataToReport, cif_read, updatedRow)
                
            else:
                self.insertToOutputData(self.processedData.inwardData.dataToManual, cif_read, updatedRow)
                
    
    
    def run(self):
        
        self.distributeTransaction()
        return self.processedData
