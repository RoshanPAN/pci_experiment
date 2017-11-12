sleeptime=1 
for i in 5 10 5 10 5 1
	do
		sudo ifconfig eno1 down && echo "stop network" && date
		sleep $sleeptime
		sudo ifconfig eno1 up  && echo "recover network" && date
		sleep $i
	done
