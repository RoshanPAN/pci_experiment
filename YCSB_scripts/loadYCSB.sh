#!/bin/bash
loadname="workloady"
cd $YCSB_PREFIX
$YCSB_PREFIX/bin/ycsb load hbase12 -P $YCSB_PREFIX/workloads/${loadname} -cp $HBASE_PREFIX/conf -p table=usertable -p columnfamily=family
cd -
echo "run ${loadname}"
