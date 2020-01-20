#!C:\Python27\python.exe -u
#!/usr/bin/env python
#written by Keith Baldwin 

import getpass
import sys
import time
import paramiko
from datetime import datetime

# Set Username and Password and DNA Center node
username = "maglev"
password = ""
DNAC = ""
today = datetime.now()
date_time = today.strftime("%m/%d/%Y, %H:%M:%S")
ERRORFLAG = ["0","0","0"]
CLOUDURLS = ["www.ciscoconnectdna.com","cdn.ciscoconnectdna.com","registry.ciscoconnectdna.com","registry-cdn.ciscoconnectdna.com","software.cisco.com","cloudsso.cisco.com","cloudsso1.cisco.com","cloudsso2.cisco.com","apiconsole.cisco.com","api.cisco.com","apx.cisco.com","sso.cisco.com","apmx-prod1-vip.cisco.com","apmx-prod2-vip.cisco.com","tools.cisco.com","www.mapbox.com","tiles.mapbox.com"]

#  Open files with list of SERVICES and RESULTS file
print("DNA CENTER CLOUD CONNECTIVITY TESTS\n")
DNAC = raw_input("Enter IP Address of DNA Center: ")
password = raw_input("Enter password for MAGLEV account: ")
print("\n\nPlease Standby - preparing the report...\n")

#  Open files with list of SERVICES and RESULTS file
f2 = open ("RESULTS-DNAC-CLOUD-SERVICES.txt", "a")
f2.write("\n\n")
f2.write("DNA CENTER CONNECTIVITY TESTS TO NODE: " + (DNAC) + " @ " + (date_time) + "\n\n")

#  Connect to DNA Center to run connectivity tests
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=(DNAC),port=2222,username=username,password=password)
remote_connection = ssh_client.invoke_shell()
remote_connection.send("\n")
connection_output = remote_connection.recv(65535)
time.sleep(1)

# Time Service Tests to ensure correct time
f2.write("Time Service Tests:\n")
remote_connection.send("timedatectl status \n\n")
time.sleep(3)
output = remote_connection.recv(65535)
if "NTP synchronized: yes" in output:
	f2.write("NTP Synchronized - success...\n")
else:
	f2.write("NTP Synchronized - failure...\n")
	ERRORFLAG[0] = "1"
remote_connection.send("date \n\n")
time.sleep(3)
f2.write("\n\n")

# NSLookup Tests to ensure services are resolved
f2.write("NS Lookup Tests:\n")
URL = ""

for URL in CLOUDURLS:
	output = ""
	remote_connection.send("nslookup " + (URL) +"\n")
	time.sleep(3)
	output = remote_connection.recv(65535)
	if "can't find" in output:
		f2.write("test to " + (URL) + " failure...\n")
		ERRORFLAG[1] = "1"
	else:
		f2.write("test to " + (URL) + " success...\n")

f2.write("\n\n")

URL = ""
# Connection Tests to ensure services are fully reachable
f2.write("Connection URL Tests:\n")

for URL in CLOUDURLS:
	output = ""
	remote_connection.send("telnet " + (URL) +" 443\n")
	time.sleep(3)	
	remote_connection.send("^] \n")
	remote_connection.send("close \n")
	time.sleep(3)	
	output = remote_connection.recv(65535)
	if "Connected to" in output:
		f2.write("test to " + (URL) + " success...\n")
	else:
		f2.write("test to " + (URL) + " failure...\n")
		ERRORFLAG[2] = "1"

f2.write("\n\n")

# Connection Summary
f2.write("Connection URL Tests:\n")
print("\n\nConnection URL Tests:\n")

if ERRORFLAG[0] == "1" :
	f2.write("NTP Synchronization issue - check Firewall settings and NTP Server IP\n")
	print("NTP Synchronization issue - check Firewall settings and NTP Server IP\n")
if ERRORFLAG[1] == "1" :
	f2.write("DNS Resolution issue - check DNS IP's, DNS Filtering, and Firewall Settings\n")
	print("DNS Resolution issue - check DNS IP's, DNS Filtering, and Firewall Settings\n")
if ERRORFLAG[2] == "1" :
	f2.write("URL Connection issue - Filtering and Proxy Settings, and Firewall Settings\n")
	print("URL Connection issue - Filtering and Proxy Settings, and Firewall Settings\n")
if '1' not in ERRORFLAG :
    f2.write("Cloud Connectivity Fully Operational\n")
    print("Cloud Connectivity Fully Operational\n")

f2.close()

# Close Connection
time.sleep(5)
ssh_client.close
