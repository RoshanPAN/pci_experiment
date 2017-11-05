sudo wget http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo
sudo sed -i s/\$releasever/6/g /etc/yum.repos.d/epel-apache-maven.repo
sudo yum install -y apache-maven
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python get-pip.py
pip install argparse
sudo yum install git
cd /usr/local
git clone git://github.com/brianfrankcooper/YCSB.git
cd YCSB
mvn -pl com.yahoo.ycsb:hbase12-binding -am clean package
echo "All setting up completed, need insert test table manully in ./hbase shell"
echo "hbase(main):001:0> n_splits = 200 # HBase recommends (10 * number of regionservers)"
echo "create 'usertable', 'family', {SPLITS => (1..n_splits).map {|i| "user#{1000+i*(9999-1000)/n_splits}"}}"
