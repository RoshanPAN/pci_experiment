#!/bin/bash
workname="workloady"
cd $YCSB_PREFIX
bin/ycsb run hbase12 -P workloads/${workname} -cp $HBASE_PREFIX/conf -p table=usertable -p columnfamily=family
cd -
echo "run ${workname}"
