#SMB time - which needs to be solved once we are up and running on linux
#    https://trello.com/c/l35E3fZW
# sudo apt-get -f -y install samba samba-common-bin
# cat /home/pi/BrewComputer2/Setup/Files/smb.conf | sudo tee -a /etc/samba/smb.conf
# sudo service smbd restart

# evdev needed for python
sudo apt-get -f -y install python-pip
sudo apt-get -f -y install python-dev
sudo pip install evdev