#!/usr/bin/python 
import mysql.connector as mariadb

try: 
	mariadb_connection = mariadb.connect(user='root', password='dbpass', database='molecularC')
	cursor = mariadb_connection.cursor()
	
except:
	print "Error Connecting to Database!"
