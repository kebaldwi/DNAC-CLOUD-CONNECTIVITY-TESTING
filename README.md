# DNAC-CLOUD-CONNECTIVITY-TESTING

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

# Appendix - Installation Instructions

Python 2.7.16 is installed by default on MAC. To install pip do the following:

sudo easy_install pip

To install Crypto and Paramiko after that do the following:

sudo pip install Crypto
sudo pip install paramiko
sudo pip install netmiko (optional)
