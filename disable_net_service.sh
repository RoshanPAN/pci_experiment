sleeptime=5
sudo systemctl stop NetworkManager.service
sleep sleeptime
sudo systemctl start NetworkManager.service
