#!/usr/bin/python
#coding: UTF-8
import os
import MySQLdb

host = 'localhost'
username = 'root'
passwpord = 'root'

class SQL_Operation:

    def __init__(self):
        self.data = []
        self.cursor = ''
        self.db = ''


    def connectToServer(self, database):

        #Connect to MySQL    
        self.db = MySQLdb.connect(host, username, password, database)
        self.cursor = self.db.cursor()

    def queryData(self, sql):
        
        self.cursor.execute(sql)

        self.data = self.cursor.fetchall()


    def closeSQLConnection(self):

        self.db.close()


    def run(self, database, sql):

        self.connectToDatabase(database)
        self.queryData(sql)
        self.closeSQLConnection()

