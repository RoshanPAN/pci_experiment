#!/bin/bash
workname="workloady"
cd $YCSB_PREFIX
stdbuf -o0 bin/ycsb run hbase12 -P workloads/${workname} -cp $HBASE_PREFIX/conf -p table=usertable -p columnfamily=family -threads 4 -s 2>&1 | tee -a /usr/local/pci_experiment_volume/YCSB_redirect.log
cd -
echo "run ${workname}"
cp /usr/local/YCSB.log /usr/local/pci_experiment_volume/YCSB_throughput.log && \
	printf "\n YCSB.log copied into volume /usr/local/pci_experiment_volume "
