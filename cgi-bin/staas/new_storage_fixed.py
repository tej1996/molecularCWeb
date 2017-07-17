#!/usr/bin/python

import os,cgi,json,sys,commands
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import dbconnect

print "Content-Type: application/json\n\n"

formdata=cgi.FieldStorage()
result={}
#taking create object fixed form data
d_name=formdata.getvalue("drive-name")
d_size=formdata.getvalue("drive-size")
username=formdata.getvalue("username")

try:
	# checking if drivename exists or not
	dbconnect.cursor.execute("SELECT drivename from users_staas WHERE drivename=%s", (d_name,))
	rows_dnames = dbconnect.cursor.fetchall()
	num_rows_drive = dbconnect.cursor.rowcount

	# retrieving the userid of current user
	dbconnect.cursor.execute("SELECT id from users WHERE username=%s", (username,))
	rows_userid = dbconnect.cursor.fetchall()
	num_rows_userid = dbconnect.cursor.rowcount

	if num_rows_userid == 1:

		if num_rows_drive == 0:

			# creating Logical Volume by the name of client's drive
			lv_s,lv_o = commands.getstatusoutput('sudo lvcreate  --name  ' + d_name + '  --size ' + d_size + 'M  m_vol_grp  -y')
			if lv_s != 0:
				result['status'] = 'Drive Name exists, please change the name!'
			else:

				# formatting client's drive with ext4
				commands.getstatusoutput('sudo mkfs.ext4   /dev/m_vol_grp/' + d_name)

				# creating mount point
				mk_s,mk_o = commands.getstatusoutput('sudo mkdir   /mnt/' + d_name)
				if mk_s != 0:
					commands.getstatusoutput('sudo rmdir   /mnt/' + d_name)
					commands.getstatusoutput('sudo mkdir   /mnt/' + d_name)
				commands.getstatusoutput('sudo chmod 777  /mnt/' + d_name)
				# mounting drive locally
				mnt_s,mnt_o = commands.getstatusoutput('sudo mount  /dev/m_vol_grp/' + d_name + '  /mnt/' + d_name)
				if mnt_s != 0:
					commands.getstatusoutput('sudo umount  /mnt/' + d_name)
					commands.getstatusoutput('sudo mount  /dev/m_vol_grp/' + d_name + '  /mnt/' + d_name)

				#install samba on server
				in_s,in_o=commands.getstatusoutput("sudo yum install samba* -y")
				if in_s!=0:
					result['status']="Samba install Error @ server!"
				else:
					commands.getstatusoutput("sudo systemctl enable smb")
					# making entry in samba configuration file at /etc/samba/smb.conf
					entry = '\n['+d_name+'_'+username+']\npath = /mnt/'+d_name+'\nwritable = yes\nbrowsable = yes\nvalid users = '+username+'\npublic = no\ncreate mask = 0777\ndirectory mask = 0777\n\n'

					# appending this entry var to /etc/samba/smb.conf
					file_smb = open('/etc/samba/smb.conf', 'a+')
					file_smb.write(entry)
					file_smb.write("\n")
					file_smb.close()
					status,output=commands.getstatusoutput("sudo systemctl reload smb")
					dtype="fixed"
					dbconnect.cursor.execute("INSERT into users_staas(uid,drivename,drivesize,dtype) VALUES(%s,%s,%s,%s)",(rows_userid[0][0], d_name, d_size+' MB', dtype))
					dbconnect.mariadb_connection.commit()
					dbconnect.mariadb_connection.close()

					sharename=d_name+'_'+username

					#client_file_entry='rmdir \media\\'+sharename+'\nread -p "Enter your username: " user_name\nmount //192.168.122.152/'+sharename+' /media/'+sharename+' -o username=user_name'
					os.system("echo 'rmdir /media/"+sharename+"\n'>>/var/www/html/staas/"+sharename+".sh")
					os.system("echo 'mkdir /media/"+sharename+"\n'>>/var/www/html/staas/"+sharename+".sh")
					os.system("echo 'read -p \"Enter your username: \" user_name\n'>>/var/www/html/staas/"+sharename+".sh")
					os.system("echo 'mount //192.168.122.152/"+sharename+"  /media/"+sharename+" -o username=$user_name\n'>>/var/www/html/staas/"+sharename+".sh")


					#commands.getstatusoutput("sudo echo -e "+client_file_entry+" > /html/staas/"+sharename+".sh")
					commands.getstatusoutput("sudo chmod 777 /var/www/html/staas/"+sharename+".sh")
					commands.getstatusoutput("sudo tar cf /var/www/html/staas/"+sharename+".tar -C /var/www/html/staas/  "+sharename+".sh")
					commands.getstatusoutput("sudo rm /var/www/html/staas/"+sharename+".sh")

					if status == 0:
						result['status']=1
						result['filename']=sharename+".tar"
					else:
						result['status']=0
		else:
			result['status']=2


except dbconnect.mariadb.Error as err:
	result['status']=format(err)

print json.dumps(result)
