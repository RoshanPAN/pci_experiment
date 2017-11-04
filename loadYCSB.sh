#!/bin/bash
loadname="workloada"
/usr/local/YCSB/bin/ycsb load hbase12 -P workloads/${loadname} -cp /usr/local/hbase-1.2.6/conf -p table=usertable -p columnfamily=family
echo "run ${loadname}"
