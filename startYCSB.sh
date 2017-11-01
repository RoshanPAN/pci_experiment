#!/bin/bash
workname="workloadmy"
cd /usr/local/YCSB
bin/ycsb run hbase12 -P workloads/${workname} -cp /usr/local/hbase-1.2.6/conf -p table=usertable -p columnfamily=family
echo "run ${workname}"
