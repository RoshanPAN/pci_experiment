#!/bin/bash
workname="workloady"
cd $YCSB_PREFIX
bin/ycsb run hbase12 -P workloads/${workname} -cp $HBASE_PREFIX/conf -p table=usertable -p columnfamily=family -thread 4
cd -
echo "run ${workname}"
cp /usr/local/YCSB.log /usr/local/pci_experiment_volume/YCSB_throughput.log && \
	printf "\n YCSB.log copied into volume /usr/local/pci_experiment_volume "
