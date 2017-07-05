#!/usr/bin/python

import cgi
import commands
import dbconnect
import json
import os
import pwd

print "Content-Type: application/json\n\n"

#received user signup form details
form_register=cgi.FieldStorage()
result={}
try: 
	#taking username & password from signup form
    	email=form_register.getvalue('remail').lower().strip()
	username=form_register.getvalue('rusername').lower().strip()
	password=form_register.getvalue('rpassword').lower().strip()

	#checking if username or email exists
	dbconnect.cursor.execute("SELECT email,username from users WHERE email=%s || username=%s", (email, username))
	rows= dbconnect.cursor.fetchall()
    	num_rows= dbconnect.cursor.rowcount
	
	try:
		luser=pwd.getpwnam(username)
		if luser:
			result['status'] = 0
	except:
		if num_rows==0:
			#insert user entry into database
			dbconnect.cursor.execute("INSERT into users(email,username,password) VALUES(%s,%s,%s)", (email, username, password))
	    		dbconnect.mariadb_connection.commit()
			dbconnect.mariadb_connection.close()

			os.system('sudo adduser '+username)
			commands.getstatusoutput('echo '+password+'| sudo passwd '+username+ ' --stdin')
			commands.getstatusoutput('printf '+password+'\n'+password+'\n | sudo smbpasswd -a '+username)
			#setting status in json object
			result['status'] = 1
		else:
			result['status'] = 0
except: 
	result['status'] = 2

print json.dumps(result)
