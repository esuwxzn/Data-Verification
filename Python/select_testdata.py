#!/usr/bin/python
#coding:UTF-8

import MySQLdb
import random

host = "localhost"
username = "root"
password = "root"

DATABASE = "TEST"
TABLE = "TESTDATA"

#Connect to MySQL    
db = MySQLdb.connect(host, username, password, DATABASE)

cursor = db.cursor();

#Select the database
#sql = "USE " + DATABASE
#cursor.execute(sql)

sql = "SELECT CIF, AMOUNT, CURRENCY FROM %s" % TABLE

cursor.execute(sql)
data = cursor.fetchall()

SUM = 0

for row in data:
    #print row
    CIF_READ = row[0]
    AMOUNT_READ = row[1]
    CURRENCY_READ = row[2]
    
    SUM += AMOUNT_READ * CURRENCY_READ
    print SUM

db.close()
