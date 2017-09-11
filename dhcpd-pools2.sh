## CM The intention of this script is to:
##	1.	Read in the routing table from CCR1 which is prepared by the CCR every 15 minutes.
## 	2.	Dump used leases to a file
##	3.	Iterate through each route and find hosts with a lease
##

baseDir=/root/newDhcpdPools
log=$baseDir/leaseAnalysis.log
currDate=$(date +%y%m%d%H%M)
report=$baseDir/publicSubnetsReport.tab

## Get the CCR1 routing table
scp pnetadmin@10.1.1.63://CCR1Routes.terse.txt $baseDir/CCR1Routes.terse.txt
cp $baseDir/CCR1Routes.terse.txt $baseDir/CCR1Routes.terse1.txt
## Write new routing table wich in the final format the Python script will use. We don't want comments and /32 routes.
grep -v "#" $baseDir/CCR1Routes.terse1.txt | grep -v "/32"> $baseDir/CCR1Routes.terse.txt

clear
echo "Analysing Leases. Please wait......."
echo ""

subnetFile=/root/leaseFilesAllServers/CCR1Routes.terse.txt
pythonScriptOutput=/root/leaseFilesAllServers/leasesOutput.csv
/root/parseLeases_dhcpd-pools.py > activeLeases
/root/newDhcpdPools/analyseCCR1_Routes.py  
/root/newDhcpdPools/analyseCCR1_Routes.py  > dhcpd-poools.txt &
echo ""
echo "Results have been saved to dhcpd-poools.txt"
echo "Tip: use '| sort -k 7,7' to sort by CMTS"
echo ""
