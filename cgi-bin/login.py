#!/usr/bin/python

import cgi,json, dbconnect

print "Content-Type: application/json\n\n"

#received user login form details
form_login=cgi.FieldStorage()
result={}
try: 
	#taking username & password from form
	username=form_login.getvalue('lusername').lower().strip()
	password=form_login.getvalue('lpassword').lower()

	#checking for authentication from db
	dbconnect.cursor.execute("SELECT username from users WHERE username=%s && password=%s",(username,password))
	row=dbconnect.cursor.fetchall()		
	num_rows=dbconnect.cursor.rowcount

	#checking if user exists and storing status in json object
	if num_rows!=0:
		result['status'] = 1
		#row will be a list of username
		result['username'] = row[0][0]
	else:
		result['status'] = 0

except:
	result['status'] = 2

print json.dumps(result)
