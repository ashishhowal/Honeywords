# Script to check the status of port 7812
while true
do
	clear
	netstat -anop | grep 7812;
	sleep 0.3
done
