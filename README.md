# pci_experiment
PCI Project Experiment Related Repository

memory_fill.c 
occupy memory for a certain amount of time "sleep(XXX);"
i in for loop is amount of mbs that will be occupied.
compile command: gcc memory_fill.c -o memory_fill
run command: ./memory_fill

disk/iops 
fill all io read to slow down hbase operation.

disable_net_service.sh
disable net service using systemd api for a period of time(can be adjusted in) to mimic a network error.

modifyYCSB.sh
shell script that replace YCSB files with modifies YCSB files.
1. replace YCSB file that can log throughputs into file(output file path can be specified in ycsbClientModified.java line 699).
2. replace YCSB starter to create a loop that perform hbase reading and updating periodly(reading and updating 1000 item 1 time). (I'm still thinking if this is good enough or edit YCSB to do a continues operations and record time delta to calculate throughput is better.)
