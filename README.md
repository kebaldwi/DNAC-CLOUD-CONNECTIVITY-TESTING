# DNAC-CLOUD-CONNECTIVITY-TESTING ver 2

This code uses python to help with installations of DNAC Clusters in Enterprise networks and lab environments. Additionally, provides a cloud connectivity report and lets you know whether the cloud connectivity is failing because of one of the following reasons:

1. NTP
2. DNS Resolution
3. IP reachability
4. Proxy Filtering
5. Firewall Filtering
6. DNS Filtering

To run this code, you will need an instance of Cisco DNA Center and a python environment running 2.7 which is installed by default on MAC OS. You will need to install pip, and the Crypto and Paramiko modules.

When this script it run it will ask for the IP address of the node please use either the VIP address or the node address if a single appliance. It will then ask for the MAGLEV password which you entered when building the node.

After that the testing will commence and it will run various tests, checking NTP synchronization, DNS resolution, IP and URL  connectivity to cloud services with simulated 443 traffic.

It will then provide a report of success or failures along with suggested remediation steps if required.

# Installation Instructions MAC OS

Python 2.7.16 is installed by default on MAC. To install pip do the following:

1. sudo easy_install pip

To install Crypto and Paramiko after that do the following:

1. sudo pip install Crypto
2. sudo pip install paramiko
3. sudo pip install netmiko (optional)

# Installation Instructions Windows

There is an all in one installer package. Follow the instructions and read all the important points paying attention to installing for all users, changing the directory to a directory on the root of your drive and environmental variables. Follow the link here:

https://www.python.org/downloads/windows/

There are many methods for getting Pip installed, but my preferred method is the following:

Download get-pip.py to a folder on your computer. Open a command prompt window and navigate to the folder containing get-pip.py. Then run python get-pip.py. This will install pip.

Once pip is installed... If you followed the Python installation instructions above, then you've already got the pip install location (default = C:\Python27\Scripts) in your Windows' PATH ENVIRONMENT VARIABLE. If you did not follow those steps, refer to them above now.

Then in Python run the following:

1. pip install Crypto
2. pip install paramiko
3. pip install netmiko (optional)
