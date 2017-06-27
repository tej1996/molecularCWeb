#!/usr/bin/python

import os,cgi,json

print "Content-Type: application/json\n\n"

formdata=cgi.FieldStorage()
result={}
#taking create object fixed form data
d_name=formdata.getvalue("drive-name")
d_size=formdata.getvalue("drive-size")

	
# client_ip will contain client's ip address  
client_ip = 

# creating Logical Volume by the name of client's drive  
lv_o = os.system('lvcreate  --name  '+d_name+'  --size '+d_size+'M  m_vol_grp  -y')
if lv_o!=0:
	result['status']='2'exists
	break

# formatting client's drive with ext4  
os.system('mkfs.ext4   /dev/m_vol_grp/'+d_name)

# creating mount point  
mk_o = os.system('mkdir   /mnt/'+d_name)
if mk_o!=0:
	os.system('rmdir   /mnt/'+d_name)
	os.system('mkdir   /mnt/'+d_name)

# mounting drive locally  
mnt_o = os.system('mount  /dev/m_vol_grp/'+d_name+'  /mnt/'+d_name)
if mnt_o!=0:
	os.system('umount  /mnt/'+d_name)
	os.system('mount  /dev/m_vol_grp/'+d_name+'  /mnt/'+d_name)

# Starting NFS server configuration  
nfs_o = os.system('yum  install  nfs-utils  -y')
if nfs_o!=0:
	result['status']=3nfsinstall error
	break

# making entry in Nfs export file 
entry="/mnt/"+d_name+"  "+client_ip+"(rw,no_root_squash)"

# appending this entry var to /etc/exports file 
file_exp = open('/etc/exports','a+')
flag_exist=0
#checking if entry already exists or not	
for line in file_exp:	
	if entry in line:
		flag_exist=1
		break

if flag_exist != 1:		
	file_exp.write(entry)
	file_exp.write("\n")

file_exp.close()	
# finally  starting  nfs  service  and service  persistant 
#os.system('systemctl   restart  nfs-server')
os.system('systemctl   enable  nfs-server')

check_nfs_update = os.system('exportfs  -r')

if  check_nfs_update  ==  0 :
	result['status']=1success

else :
	result['status']=0 error

