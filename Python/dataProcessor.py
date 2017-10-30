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

        queryType = queryInfo['queryType']

        table = queryInfo['table']

        if queryType == 'EXCHANGERATE':
            
            currency = queryInfo['currency']
            date = queryInfo['date']
            #table = self.database.exchangeRateTable
            return 'SELECT %s FROM %s WHERE DATE = %s' % (currency, table, date)
        
        elif queryType == 'TAXCODE':
            key = queryInfo['key']
            CIF = queryInfo['CIF']
            return 'SELECT %s FROM %s WHERE CIF  = %s' % (key, table, CIF)

        elif queryType == 'CIF':
            customer_acc_key = queryInfo['customer_acc_key']
            account_number = queryInfo['account_number']
            cif_key = queryInfo['cif_key']
            return 'SELECT %s FROM %s WHERE %s = %s' % (cif_key, table, customer_acc_key, account_number)

    def retriveExchangeRate(self, currency, date):

        SQL = sqlOperation()

        queryInfo = {'queryType':'EXCHANGERATE', 'currency':currency, 'date':date, 'table':self.database.exchangeRate.exchangeRateTable}

        sql = self.generateQuerySQL(**queryInfo)
        
        SQL.run(self.database.exchangeRate.exchangeRateDatabase, sql)
       
        if len(SQL.data) != 0:
            return SQL.data[0][0]
        else:
            return ''

     
    def retrieveTaxCode(self, CIF):

        SQL = sqlOperation()

        queryInfo = {'queryType':'TAXCODE', 'key':'TAX_C', 'CIF':CIF, 'table':self.database.customerInfo.customerInfoTable}
        sql = self.generateQuerySQL(**queryInfo)
        
        SQL.run(self.database.customerInfo.customerInfoDatabase, sql) 
       

        if len(SQL.data) != 0: 
            return SQL.data[0][0]
        else:
            return ''



    def retrieveCIF(self, account_number):

        SQL = sqlOperation()

        queryInfo = {'queryType':'CIF', 'customer_acc_key':'INVM_MEMB_CUST_AC', 'account_number':account_number, 'cif_key':'CD03_CUSTOMER_NO', 'table':self.database.invm.invmTable}
        sql = self.generateQuerySQL(**queryInfo)
        
        SQL.run(self.database.customerInfo.customerInfoDatabase, sql) 
       
        if len(SQL.data) != 0:
            return SQL.data[0][0]
        else:
            return ''


    def updateRow(self, Type, row):
    
        if Type == 'INWARD':
            return row
        
        elif Type == 'OUTWARD':
            return row




    def convertCurToSEK(self, valueDate, currency, fx_rate_index, SEK_index, row):
        
        fx_rate = self.retriveExchangeRate(currency, valueDate)
        
        originalList = list(row)
        originalList.insert(fx_rate_index, fx_rate)
        originalList.insert(SEK_index, float(originalList[3]) * fx_rate)
        #print originalList
        return tuple(originalList)


    #def insertCIFandTaxCode(self, CIF, TAX_C):





    def insertToOutputData(self, outputData, key, value):
        if not outputData.has_key(key):
            outputData[key] = [value,]
        else:
            outputData[key].append(value)
    



    def processInwardData(self, inputData):

        for row in inputData: 
            valueDate    = row[0]
            currency     = row[4]
            cif_read     = row[5]
            from_country = row[2]
            fx_rate_index = 6
            SEK_index = 7

            updatedRow = self.updateRow('INWARD', row)

            updatedRow = self.convertCurToSEK(valueDate, currency, fx_rate_index, SEK_index, row)

            if cif_read != '' and from_country != 'SE' and from_country != '00':
                self.insertToOutputData(self.processedData.inwardData.dataToReport, cif_read, updatedRow)
                
            else:
                self.insertToOutputData(self.processedData.inwardData.dataToManual, cif_read, updatedRow)


    def processOutwardData(self, inputData):

        for row in inputData:
            print row
            valueDate    = row[0]
            to_country   = row[2]
            currency     = row[4]
            account_number = row[5]
            fx_rate_index = 8
            SEK_index = 9
            
            updatedRow = self.updateRow('OUTWARD', row)
            
            #if account_number != 'NEED_TO_BE_CHECKED' or account_number != '':
            if account_number.isdigit():
                cif_read = self.retrieveCIF(account_number) 
                
                if len(cif_read) != 0:
                    tax_code = self.retrieveTaxCode(cif_read)
                else:
                    tax_code = ''
            else:
                cif_read = ''
                tax_code = ''
            

            #updatedRow = self.insertCIFandTaxCode(cif_read, tax_code, row)
            #updatedRow = self.convertCurToSEK(valueDate, currency, fx_rate_index, SEK_index, row)

            updatedRow = row

            #if cif_read != '' and to_country != 'SE' and from_country != '00':
            #    self.insertToOutputData(self.processedData.inwardData.dataToReport, cif_read, updatedRow)
                
            #else:
            #    self.insertToOutputData(self.processedData.inwardData.dataToManual, cif_read, updatedRow)

    def distributeTransaction(self):
        #self.processInwardData(self.inputData.inwardData)
        self.processOutwardData(self.inputData.outwardData)
    
    
    def run(self):
        
        self.distributeTransaction()
        #self.distributeTransaction('OUTWARD')
        return self.processedData
