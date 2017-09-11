#!/usr/bin/python
## CM 08-09-17 My version of DHCPD-Pools
import math
import re
subnetPosition = 0
subnet = "0"
subnets = "0"
spacer = "\t\t"
classDir="classes"
seperater = "-----------------------------------------------------------------------------------"
#print (header)
#print (seperater)
import re
import os
os.system('clear') 
print ""
print ""
print "Subnet\t" + "\tMASK" + "\tBOUND\t" + "FREE\t" + "Used %" + "\tFree % " + "\tNext Hop"  + "\tArea"
print seperater
for rawSubnets in open("/root/newDhcpdPools/CCR1Routes.terse.txt",'r'):
	## Extact the info from the route read from file above.
	found = 0
	process = 1
	subnet = rawSubnets[rawSubnets.find(" dst-address=")+1:].split("=")[1].split(" ")[0].split("/")[0]
	mask = rawSubnets[rawSubnets.find(" dst-address=")+1:].split("=")[1].split(" ")[0].split("/")[1]
	gateway = rawSubnets[rawSubnets.find("way=")+1:].split()[0]
	nextHop = rawSubnets[rawSubnets.find("via")+4:].split()[0]
	gate = gateway.split("=")[1]
	## Its nice to have the decimal mask also, can't see a case/switch equivilant for Python so will use if elif
	if mask == "23":
		hosts = 510
		decMask = "255.255.254.0"
	elif mask == "24":
		hosts = 254
		decMask = "255.255.255.0"
	elif mask == "25":
		hosts = 126
		decMask = "255.255.255.128"
	elif mask == "26":
		hosts = 62
		decMask = "255.255.255.192"
	elif mask == "27":
		hosts = 30
		decMask = "255.255.255.224"
	elif mask == "28":
		hosts = 14
		decMask = "255.255.255.240"
	elif mask == "29":
		hosts = 6
		decMask = "255.255.255.248"
	elif mask == "30":
		hosts = 2
		decMask = "255.255.255.252"
		process = 1
	elif mask == "32":
		hosts = 1
		decMask = "255.255.255.255"
		process = 1
	## Cheating here if the mask is 23 we process as a 24
	if mask == "23":
		hosts = 254
		mask = "24"
		decMask = "255.255.255.0"
	## Now we need to break up the subnet ID into 4 quads so we can calculate the first and last ip
	splitIP=subnet.split(".")
        quad0 = splitIP[0]
        quad1 = splitIP[1]
        quad2 = splitIP[2]
        quad3 = splitIP[3]
	checked = str(quad0) + "."  + str(quad1) + "." + str(quad2) + "." + str(quad3)
	# Calculate first and last IP
	firstIP = int(quad3) + 1
	lastIP  = int(quad3) + int(hosts)
	#print str(firstIP) + " is the firstIP" 
 	#print "Subnet:" + subnet + "\t|\t" + mask + "\t|\t" + "First IP:" + str(firstIP) + "\t|\t"  + " Last IP:" + str(lastIP)
	## A for loop which runs hosts times, this is where we lookup "/root/leaseFilesAllServers/leasesOutput.csv" for a matching ip.
	
	found = 0
	notFound = 0
	for check in range(hosts):
		#print "Check is " + str(check)
		newCheck = check + firstIP
		#print "New Check is " + str(newCheck)
                ip = str(quad0) + "."  + str(quad1) + "." + str(quad2) + "." + str(newCheck)
		#print "Debug: Processing IP:" + ip
		## Code needed to count leases
		## We need to open activeLeases.1709080941 and read each line to a variable variable.split()[0] is the IP address
		for leases in open("/root/newDhcpdPools/activeLeases",'r'):
			checkIP = leases.split()[0]
			#print "Debug: Checking " + ip + " against " + checkIP
			if checkIP == ip:
				#print ip + " is leased"
				found = found + 1
				break
	free = hosts - found
	perCentUsed = float(found) / float(hosts) * 100
	perCentFree = 100 - perCentUsed
	if found <> 0:
		#print subnet + "/" + mask + "\t\tLeased:" + str(found) + "\tAvailable:" + str(notFound) + "\tArea: " + gate + "\t" + nextHop
		print subnet + "\t/" + mask + "\t" + str(found) + "\t" + str(free) + "\t" + str(round(perCentUsed, 0)) + "\t" + str(round(perCentFree, 0)) + "\t" + gate + "\t" + nextHop

print ""
print "Remember to run synch-dhcpd-pools2.sh to work with the latest routing table."
print "Manually check overlaping routes, EG a /24 might be configured on MishBridged but a child subnet routes to Knock."
print ""	
