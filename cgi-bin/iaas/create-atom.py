#!/usr/bin/python

import cgi,json,commands,os,time,sys, pyqrcode
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import dbconnect
from random import randint


print "Content-Type: application/json\n\n"

formdata=cgi.FieldStorage()
result={}
#taking create atom form data
osname=formdata.getvalue("os")
grp=formdata.getvalue("grp")
atomname=formdata.getvalue("atomname")
username=formdata.getvalue("username")

#setting values for each group
if grp=="grp1":
	ram="256"
	cpucore="1"
	hdd="1"
elif grp=="grp2":
	ram="1024"
	cpucore="1"
	hdd="2"
elif grp=="grp3":
	ram="1024"
	cpucore="2"
	hdd="5"
elif grp=="grp4":
	ram="1024"
	cpucore="2"
	hdd="10"	

avail=False
if osname=="ubuntu":

	try:
		#checking if atomname exists or not
		dbconnect.cursor.execute("SELECT atomname from users_iaas WHERE atomname=%s", (atomname,))
		rows_atom = dbconnect.cursor.fetchall()
		num_rows_atom = dbconnect.cursor.rowcount

		#retrieving the userid of current user
		dbconnect.cursor.execute("SELECT id from users WHERE username=%s",(username,))
		rows_userid = dbconnect.cursor.fetchall()
		num_rows_userid = dbconnect.cursor.rowcount

		#checking for port if available or not,if not generate new and check again
		while avail == False:
			websockify_port = randint(6000, 6800)
			vnc_port = randint(5900, 5999)

			# retrieving the vnc_port & websockify_port from db
			dbconnect.cursor.execute("SELECT vnc_port,websockify_port from users_iaas WHERE vnc_port=%s || websockify_port=%s", (vnc_port,websockify_port))
			rows_ports = dbconnect.cursor.fetchall()
			num_rows_ports = dbconnect.cursor.rowcount

			#checking the specified port already binded or not
			web_port_status,web_port_out=commands.getstatusoutput("netstat -nltu | grep "+str(websockify_port))
			vnc_port_status,vnc_port_out=commands.getstatusoutput("netstat -nltu | grep "+str(vnc_port))

			if num_rows_ports==0:
				if web_port_status!=0 and vnc_port_status!=0:
					avail=True

		if num_rows_userid == 1:

			if num_rows_atom == 0:

				#install os with virt-install
				commands.getstatusoutput('sudo qemu-img create -f qcow2 -b /var/lib/libvirt/images/generic.qcow2 /var/lib/libvirt/images/' + atomname + '.qcow2')

				ins_status,install_os = commands.getstatusoutput('sudo virt-install  --name ' + atomname + ' --ram ' + ram + ' --vcpu ' + cpucore + ' --disk path=/var/lib/libvirt/images/' + atomname + '.qcow2  --import  --graphics vnc,listen=192.168.122.1,port='+str(vnc_port)+' --noautoconsole')
				time.sleep(30)
				machine_ip=commands.getoutput("sudo virsh domifaddr "+atomname+" | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'")
				novnc_url="http://192.168.122.1:"+str(websockify_port)
				if ins_status == 0:
					# insert created atom entry into users_iaas table
					try:
						run_status="active"
						dbconnect.cursor.execute("INSERT into users_iaas(uid,atomname,osname,grpname,vnc_port,websockify_port,machine_ip,novnc_url,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (rows_userid[0][0],atomname,osname,grp,vnc_port,websockify_port,machine_ip,novnc_url,run_status))
						dbconnect.mariadb_connection.commit()
						dbconnect.mariadb_connection.close()
						os.system('sudo websockify --web=/usr/share/novnc '+str(websockify_port)+' 192.168.122.1:'+str(vnc_port)+' -D')
						qrcode = pyqrcode.create(novnc_url)
						qrcode.png("/var/www/html/iaas/qrcodes/" +username+"_"+ atomname + ".png", scale=8)
						result['status'] = "Success"
					except:
						result['status'] = "Unable to store to database!"
				else:
					result['status'] =  "Unable to install os & setup iaas"
			else:
				result['status'] = "Atom name already exists"
		else:
			result['status'] = "User does not exist!"
	except dbconnect.mariadb.Error as err:
			result['status']=format(err)

print json.dumps(result)





