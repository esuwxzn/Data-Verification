#!/usr/bin/python
#coding: UTF-8



class Data_Processor:


    def __init__(self, inputData):
        self.inputData = inputData
        self.outputDataToReport = {}
        self.outputDataToManual = {}


    def insertToOutputData(self, outputData, key, value):
        if not outputData.has_key(key):    
            outputData[key] = [value,]
        else:   
            outputData[key].append(value)

    def distributeTransaction(self):

        for row in self.inputData:
            cif_read = row[5]
            from_country = row[2]

            if cif_read != '' and from_country != 'SE' and from_country != '00':
                self.insertToOutputData(self.outputDataToReport, cif_read, row)
            else:
                self.insertToOutputData(self.outputDataToManual, cif_read, row)
                
    #def run(self, inputData):
    def run(self):
        self.distributeTransaction()
