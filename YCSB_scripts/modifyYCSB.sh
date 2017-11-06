cp ./ycsbClientModified.java /usr/local/YCSB/core/src/main/java/com/yahoo/ycsb/Client.java
cp ./ycsbModified /usr/local/YCSB/bin/ycsb
cp ./workloady $YCSB_PREFIX/workloads/workloady
printf "File replaced.\n workloady added. \n YCSB will now log throughput into /usr/local/YCSB.log"
