#!/usr/bin/python

import cgi,commands

print "Content-Type: text/html\r\n\r\n"
print ""

#received download option
saas_option=cgi.FieldStorage()
try: 
	#taking requested software name
	download=saas_option.getvalue('download')
	if download=="firefox":
		print "<meta http-equiv='refresh' content='0;url='/saas/firefox.tar'/>"
	if download=="vlc":
		print "<meta http-equiv='refresh' content='0;url='/saas/vlc.tar'/>"
	if download=="screenshot":
		print "<meta http-equiv='refresh' content='0;url='/saas/screenshot.tar'/>"
	if download=="webcam":
		print "<meta http-equiv='refresh' content='0;url='/saas/webcam.tar'/>"
	if download=="calculator":
		print "<meta http-equiv='refresh' content='0;url='/saas/calculator.tar'/>"
	if download=="openoffice":
		print "<meta http-equiv='refresh' content='0;url='/saas/openoffice.tar'/>"
except:
	print "error"
