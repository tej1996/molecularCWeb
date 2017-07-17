#!/usr/bin/python

import os,cgi,json,sys,commands,datetime
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import dbconnect

print "Content-Type: application/json\n\n"

formdata=cgi.FieldStorage()
result={}
#taking service request data
s_type=formdata.getvalue("serv-type")
username=formdata.getvalue("username")
if s_type=="python":
    shell="python"
elif s_type=="ruby":
    shell="irb"
elif s_type=="perl":
    shell="bash"
try:
    commands.getstatusoutput("sudo docker start 9b3a8ce5a")
    commands.getstatusoutput("sudo docker exec -i 9b3a8ce5a usermod -s /usr/bin/"+shell+"  "+username)
    commands.getstatusoutput("sudo systemctl start shellinaboxd")
    result['surl'] = "https://molecularc.com:4210"
    result['status']=1
except Exception as err:
    result['status']= format(err)


print json.dumps(result)