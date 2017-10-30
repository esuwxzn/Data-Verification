#!/usr/bin/python
#coding: UTF-8

from dataClasses import taxStatisticData, processedTransactionData
from sqlOperation import sqlOperation
from sqlDatabaseConf import databaseList
import re


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


    def retrieveData(self, **info):
        
        Type = info['type']

        if Type == 'CIF':
            queryInfo = {'queryType':Type, 'customer_acc_key':'INVM_MEMB_CUST_AC', 'account_number':info['account_number'], 'cif_key':'CD03_CUSTOMER_NO', 'table':self.database.invm.invmTable}
            database = self.database.customerInfo.customerInfoDatabase

        elif Type == 'TAXCODE':
            queryInfo = {'queryType':Type, 'key':'TAX_C', 'CIF':info['CIF'], 'table':self.database.customerInfo.customerInfoTable}
            database = self.database.customerInfo.customerInfoDatabase
        
        elif Type == 'EXCHANGERATE':
            queryInfo = {'queryType':Type, 'currency':info['currency'], 'date':info['valueDate'], 'table':self.database.exchangeRate.exchangeRateTable}
            database = self.database.exchangeRate.exchangeRateDatabase
        
        elif Type == 'CUSTOMERINFO':
            queryInfo = {'queryType':Type, 'key':'TAX_C', 'CIF':info['CIF'], 'table':self.database.customerInfo.customerInfoTable}
            database = self.database.customerInfo.customerInfoDatabase

        else:
            print "Unsupport query type in retrieveData()..."
            exit(0)
        

        SQL = sqlOperation()

        sql = self.generateQuerySQL(**queryInfo)
        
        SQL.run(database, sql) 
       
        if len(SQL.data) != 0:
            return SQL.data[0][0]
        else:
            return ''



    def retrieveReason(self, message):

        return re.findall(r':70:(.+?):71', message)



    def updateRow(self, **updateInfo, row):
   
        row = list(row)

        if Type == 'INWARD':
            row.append('RATE = X')
            row.append('SEK = X')
            row.append('Organisation number = X')
            row.append('Personal number = X')
            row.append('Address = X')
            row.append('Tax code = X')
        
        elif Type == 'OUTWARD':

            row[5] = updateInfo['reason']
            row.insert(6, updateInfo['CIF'])

            row.append(updateInfo['exchangeRate']
            row.append(updateInfo['SEK']
            row.append(updateInfo['org_number']
            row.append(updateInfo['personal_number']
            row.append(updateInfo['address']
        
        return tuple(row)


    def insertToOutputData(self, outputData, key, value):
        if not outputData.has_key(key):
            outputData[key] = [value,]
        else:
            outputData[key].append(value)
    



    def processInwardData(self, inputData):

        for row in inputData: 
            valueDate    = row[0]
            from_country = row[2]
            currency     = row[4]
            cif_read     = row[5]
            fx_rate_index = 6
            SEK_index = 7

            updatedRow = self.updateRow('INWARD', row)
            #print updatedRow
            updatedRow = self.convertCurToSEK(valueDate, currency, fx_rate_index, SEK_index, updatedRow)
            
            #print updatedRow
            if cif_read != '' and from_country != 'SE' and from_country != '00':
                self.insertToOutputData(self.processedData.inwardData.dataToReport, cif_read, updatedRow)
                
            else:
                self.insertToOutputData(self.processedData.inwardData.dataToManual, cif_read, updatedRow)


    def processOutwardData(self, inputData):

        for row in inputData:

            retrieveInfo = {}
            updatedInfo = {} 
            

            valueDate      = row[0]
            to_country     = row[2]
            amount         = row[3]
            currency       = row[4]
            message        = row[5]
            account_number = row[7]
            
            print row
            if account_number.isdigit():

                retrieveInfo = {'type':'CIF', 'account_number': account_number}
                cif_read = self.retrieveData(**retrieveInfo) 
                
                if len(cif_read) != 0:
                    
                    retrieveInfo = {'type':'TAXCODE', 'CIF': cif_read}
                    tax_code = self.retrieveData(**retrieveInfo)

                else:
                    tax_code = ''

            else:
                cif_read = ''
                tax_code = ''
            
            if currency != 'SEK':
                retrieveInfo = {'type':'EXCHANGERATE', 'valueData': valueDate, 'currency':currency}
                exchangeRate = self.retrieveData(**retrieveInfo)
                SEK = amount * exchangeRate
            else:
                SEK = amount
           

            #Customer Info:Org number, personal number or address
            retrieveInfo['type':'CUSTOMERINFO', 'CIF':cif_read]
            customerInfo = self.retrieveData(**retrieveInfo)


            reason = self.retrieveReason(message)
            
            updateInfo['type'] = 'OUTWARD'
            updateInfo['reason'] = reason
            updateInfo['CIF'] = cif_read
            updateInfo['exchangeRate'] = exchangeRate
            updateInfo['SEK'] = SEK 
            updateInfo['tax_code'] = tax_code
            updateInfo['org_number'] = customerInfo[0]
            updateInfo['personal_number'] = customerInfo[1]
            updateInfo['address'] = customerInfo[2]

            
            updatedRow = self.updateRow(**updateInfo, row)

            #updatedRow = self.insertCIFandTaxCode(cif_read, cif_index, tax_code, tax_code_index, updatedRow)
            #updatedRow = self.convertCurToSEK(valueDate, currency, fx_rate_index, SEK_index, row)

            #updatedRow = row

            #if cif_read != '' and to_country != 'SE' and from_country != '00':
            #    self.insertToOutputData(self.processedData.inwardData.dataToReport, cif_read, updatedRow)
                
            #else:
            #    self.insertToOutputData(self.processedData.inwardData.dataToManual, cif_read, updatedRow)

    def distributeTransaction(self):
        self.processInwardData(self.inputData.inwardData)
        self.processOutwardData(self.inputData.outwardData)
    
    
    def run(self):
        
        self.distributeTransaction()
        #self.distributeTransaction('OUTWARD')
        return self.processedData
