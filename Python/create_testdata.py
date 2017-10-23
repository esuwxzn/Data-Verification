#!/usr/bin/python
#coding: UTF-8

import MySQLdb
import random


host = "localhost"
username = "root"
password = "root"

DATABASE = "TEST"
TABLE    = "TESTDATA"
TABLE_KEY = "(CIF CHAR(30), NAME CHAR(30), TAX_FLAG CHAR(1), AMOUNT FLOAT, CURRENCY FLOAT)"
TABLE_KEY_INSERT = "(CIF, NAME, TAX_FLAG, AMOUNT, CURRENCY)"


#Connect to MySQL    
db = MySQLdb.connect(host, username, password)

cursor = db.cursor();

#Drop database if exist.
sql = "DROP DATABASE IF EXISTS %s" % DATABASE
cursor.execute(sql)

#Create the database
sql = "CREATE DATABASE %s" % DATABASE 
cursor.execute(sql)

#Select the database
sql = "USE " + DATABASE
cursor.execute(sql)

#Create a table for testing.
sql = "CREATE TABLE %s %s" % (TABLE, TABLE_KEY)
cursor.execute(sql)

TOTAL = 100

for index in range(TOTAL):

    VALUE = [] 
    
    CIF = random.randrange(10000000,99999999,8)
    NAME = random.sample('abcdefghijklmnopqrstuvwxzy', 10)
    NAME = ''.join(NAME)
    TAX_FLAG = "Y"
    AMOUNT  = random.random() * 10000;
    CURRENCY = random.random() * 10;
    
    sql = """INSERT INTO %s%s VALUE("%s", "%s", "%s", %f, %f)""" % (TABLE, TABLE_KEY_INSERT, CIF, NAME, TAX_FLAG, AMOUNT, CURRENCY)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

db.close()
