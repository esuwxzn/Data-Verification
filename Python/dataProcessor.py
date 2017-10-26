#!/usr/bin/python
#coding: UTF-8

from dataClasses import taxStatisticData, processedTransactionData

class dataProcessor:


    def __init__(self, inputData):
        self.inputData = inputData
        self.processedData = processedTransactionData()



    def insertToOutputData(self, outputData, key, value):
        if not outputData.has_key(key):    
            outputData[key] = [value,]
        else:   
            outputData[key].append(value)

    def distributeTransaction(self):

        count1 = 0
        count2 = 0
        for row in self.inputData.inwardData:
        
            cif_read = row[5]
            from_country = row[2]
        

            if cif_read != '' and from_country != 'SE' and from_country != '00':
                self.insertToOutputData(self.processedData.inwardData.dataToReport, cif_read, row)
                
            else:
                self.insertToOutputData(self.processedData.inwardData.dataToManual, cif_read, row)
                
    
    
    def run(self):
        
        self.distributeTransaction()
        return self.processedData
