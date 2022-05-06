#!/usr/bin bash

echo ""
echo "======================="
echo "Installing requirements"
echo "======================="
echo ""
sudo apt update -y
sudo apt install python -y
sudo apt install autoremove -y
pip install requests
pip install bs4
pip install urllib3
echo ""
echo "==============="
echo "Complete setup."
echo "==============="
echo ""