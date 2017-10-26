#!/usr/bin/python
#coding: UTF-8

from SQL_Operation import SQL_Operation
from Data_Processor import Data_Processor
from File_Generator import File_Generator


SQL = SQL_Operation()
SQL.run('localhost', 'root', 'root', 'CUSTOMER', 'inward', 'INWARD')

DP = Data_Processor(SQL.data)
DP.run()
#print DP.outputData
#DP = Data_Processor()
#DP.run(SQL.data)

#print DP.outputDataToReport.keys()
#print DP.outputDataToManual.keys()

#print DP.outputDataToReport.values()
#print
#print
#print DP.outputDataToManual.values()


FG = File_Generator(DP.outputDataToReport, DP.outputDataToManual)

FG.run()
