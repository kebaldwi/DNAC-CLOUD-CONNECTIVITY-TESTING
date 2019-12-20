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
ERRORFLAG = ["0","0","0","0"]
CLOUDURLS = ["www.ciscoconnectdna.com","cdn.ciscoconnectdna.com","registry.ciscoconnectdna.com","registry-cdn.ciscoconnectdna.com","software.cisco.com","cloudsso.cisco.com","cloudsso1.cisco.com","cloudsso2.cisco.com","apiconsole.cisco.com","api.cisco.com","apx.cisco.com","sso.cisco.com","apmx-prod1-vip.cisco.com","apmx-prod2-vip.cisco.com","tools.cisco.com","www.mapbox.com","tiles.mapbox.com"]
CLOUDIPS= ["35.165.49.51","99.84.101.128","50.112.227.10","99.84.101.81","104.108.99.80","173.37.144.211","72.163.4.74","173.37.144.211","54.235.187.110"
,"173.37.145.221","173.37.148.102","173.37.144.208","72.163.11.230","173.37.148.102","72.163.4.38","151.101.184.143","151.101.184.143"]

#  Open files with list of SERVICES and RESULTS file
print("DNA CENTER CLOUD CONNECTIVITY TESTS\n")
DNAC = raw_input("Enter IP Address of DNA Center: ")
password = raw_input("Enter password for MAGLEV account: ")
print("\n\nPlease Standby - preparing the report...\n")

#  Open files with list of SERVICES and RESULTS file
f2 = open ("RESULTS-DNAC-CLOUD-SERVICES.txt", "a")
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
IPADDRESS = ""

# Connection Tests to ensure Cloud IP Spaces are reachable
f2.write("Connection IP Only Tests:\n")
for IPADDRESS in CLOUDIPS:
	output = ""
	remote_connection.send("telnet " + (IPADDRESS) +" 443\n")
	time.sleep(3)	
	remote_connection.send("^] \n")
	remote_connection.send("close \n")
	time.sleep(3)	
	output = remote_connection.recv(65535)
	if "Connected to" in output:
		f2.write("test to " + (IPADDRESS) + " success...\n")
	else:
		f2.write("test to " + (IPADDRESS) + " failure...\n")
		ERRORFLAG[2] = "1"

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
		ERRORFLAG[3] = "1"

f2.write("\n\n")

# Connection Summary
f2.write("Connection URL Tests:\n")
print("\n\nConnection URL Tests:\n")

if ERRORFLAG[0] == "1" :
	f2.write("NTP Synchronization issue - check firewall and IP\n")
	print("NTP Synchronization issue - check firewall and IP\n")
if ERRORFLAG[1] == "1" :
	f2.write("DNS Resolution issue - check IP, filtering, and firewall\n")
	print("DNS Resolution issue - check IP, filtering, and firewall\n")
if ERRORFLAG[2] == "1" :
	f2.write("IP Connection issue - check routing, filtering, proxy, and firewalls\n")
	print("IP Connection issue - check routing, filtering, proxy, and firewalls\n")
if ERRORFLAG[3] == "1" :
	f2.write("URL Connection issue - filtering, proxy, and firewalls\n")
	print("URL Connection issue - filtering, proxy, and firewalls\n")
if '1' not in ERRORFLAG :
    f2.write("Cloud Connectivity Fully Operational\n")
    print("Cloud Connectivity Fully Operational\n")

f2.close()

# Close Connection
time.sleep(5)
ssh_client.close
