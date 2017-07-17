#!/usr/bin/python

import os,cgi,json,sys,commands,datetime
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import dbconnect

print "Content-Type: application/json\n\n"

formdata=cgi.FieldStorage()
result={}
#taking create new block storage form data
p_name=formdata.getvalue("part-name")
p_size=formdata.getvalue("part-size")
username=formdata.getvalue("username")

try:
	# checking if drivename/partition exists or not
	dbconnect.cursor.execute("SELECT drivename from users_staas WHERE drivename=%s", (p_name,))
	rows_dnames = dbconnect.cursor.fetchall()
	num_rows_drive = dbconnect.cursor.rowcount

	# retrieving the userid of current user
	dbconnect.cursor.execute("SELECT id from users WHERE username=%s", (username,))
	rows_userid = dbconnect.cursor.fetchall()
	num_rows_userid = dbconnect.cursor.rowcount

	if num_rows_userid == 1:

		if num_rows_drive == 0:

			# creating Logical Volume by the name of client's partition
			lv_s,lv_o = commands.getstatusoutput('sudo lvcreate  -V'+p_size+'G  --name  ' + p_name + '  --thin  m_vol_grp/m_pool1  -y')
			if lv_s != 0:
				result['status'] = 'Partition name exists, please change the name!'
			else:


				#install iscsi-target-utils on server
				in_s,in_o=commands.getstatusoutput("sudo yum install scsi-target-utils -y")
				if in_s!=0:
					result['status']="iSCSI install Error @ server!"
				else:
					commands.getstatusoutput("sudo systemctl enable tgtd")
					year=datetime.datetime.now().year
					month=datetime.datetime.now().month
					# making entry in iscsi configuration file at /etc/tgt/targets.conf
					entry = '\n<target iqn.'+str(year)+'-'+str(month)+'.molecularC.com:'+p_name+'_'+username+'>\n' \
							'      backing-store  /dev/m_vol_grp/'+p_name+'\n' \
							'</target>\n'

					# appending this entry var to /etc/tgt/targets.conf
					file_tgt = open('/etc/tgt/targets.conf', 'a+')
					file_tgt.write(entry)
					file_tgt.write("\n")
					file_tgt.close()
					status,output=commands.getstatusoutput("sudo systemctl reload tgtd")
					dtype="block"
					dbconnect.cursor.execute("INSERT into users_staas(uid,drivename,drivesize,dtype) VALUES(%s,%s,%s,%s)",(rows_userid[0][0], p_name, p_size+' GB',dtype))
					dbconnect.mariadb_connection.commit()
					dbconnect.mariadb_connection.close()

					iqn_name='iqn.'+str(year)+'-'+str(month)+'.molecularC.com:'+p_name+'_'+username
					os.system("echo 'yum install iscsi-initiator-utils -y \n'>>/var/www/html/staas/"+p_name+".sh")
					os.system("echo 'iscsiadm -m discovery -t st -p 192.168.122.152 >>/dev/null \n'>>/var/www/html/staas/"+p_name+".sh")
					os.system("echo 'iscsiadm -m node --target "+iqn_name+"  -p 192.168.122.152:3260 --login\n'>>/var/www/html/staas/"+p_name+".sh")
					os.system("echo 'rmdir /media/"+p_name+"\n'>>/var/www/html/staas/"+p_name+".sh")
					os.system("echo 'mkdir /media/"+p_name+"\n'>>/var/www/html/staas/"+p_name+".sh")
					os.system("echo 'mkfs.ext4 /dev/sdb\n'>>/var/www/html/staas/"+p_name+".sh")
					os.system("echo 'mount /dev/sdb  /media/"+p_name+"\n'>>/var/www/html/staas/"+p_name+".sh")


					os.system("sudo chmod 777 /var/www/html/staas/"+p_name+".sh")
					os.system("sudo tar cf /var/www/html/staas/"+p_name+".tar -C /var/www/html/staas/  "+p_name+".sh")
					commands.getstatusoutput("sudo rm /var/www/html/staas/"+p_name+".sh")

					if status == 0:
						result['status']=1
						result['filename']=p_name+".tar"
					else:
						result['status']=0
		else:
			result['status']=2


except dbconnect.mariadb.Error as err:
	result['status']=format(err)

print json.dumps(result)
