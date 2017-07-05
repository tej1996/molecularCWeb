#!/usr/bin/python

import cgi,json,os,sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import dbconnect


print "Content-Type: application/json\n\n"

formdata=cgi.FieldStorage()
result={}
#taking current loggedin username
username=formdata.getvalue("username")
try:
	#retrieving the userid of current user
	dbconnect.cursor.execute("SELECT id from users WHERE username=%s",(username,))
	rows_userid = dbconnect.cursor.fetchall()
	num_rows_userid = dbconnect.cursor.rowcount
	
	if num_rows_userid == 1:
		
		try:
			#retrieving all atoms list created by logged in user
			dbconnect.cursor.execute("SELECT osname,atomname,machine_ip,novnc_url from users_iaas WHERE uid=%s",(rows_userid[0][0],))
			rows = dbconnect.cursor.fetchall()
			num_rows_atoms = dbconnect.cursor.rowcount

			if num_rows_atoms!=0:
				result['data']=rows
			dbconnect.mariadb_connection.commit()
			dbconnect.mariadb_connection.close()
			result['status'] = 1
		except:
			result['status']=format(dbconnect.Error)
	else:
		result['status'] = 0
except dbconnect.Error:
		result['status']=format(dbconnect.Error)

print json.dumps(result)





