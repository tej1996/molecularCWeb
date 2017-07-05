#!/usr/bin/python

import cgi,json,commands,os,dbconnect
from random import randint
import mysql.connector as mariadb


print "Content-Type: application/json\n\n"

formdata=cgi.FieldStorage()
result={}
#taking create atom form data
username=formdata.getvalue("username")
try:
	#retrieving the userid of current user
	dbconnect.cursor.execute("SELECT id from users WHERE username=%s",(username,))
	rows_userid = dbconnect.cursor.fetchall()
	num_rows_userid = dbconnect.cursor.rowcount
	
	if num_rows_userid == 1:
		
		try:
			dbconnect.cursor.execute("SELECT osname,atomname,machine_ip,novnc_url from users_iaas WHERE uid=%s",(rows_userid[0][0],))
			rows = dbconnect.cursor.fetchall()
			num_rows_atoms = dbconnect.cursor.rowcount

			if num_rows_atoms!=0:
				result['data']=rows
			dbconnect.mariadb_connection.commit()
			dbconnect.mariadb_connection.close()
			result['status'] = 1
		except:
			result['status']=format(mariadb.Error)
	else:
		result['status'] = 0
except mariadb.Error:
		result['status']=format(mariadb.Error)

print json.dumps(result)





