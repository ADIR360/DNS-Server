#!/bin/bash
# Update system and install necessary packages
sudo apt update && sudo apt upgrade -y
sudo apt install curl unbound python3-pip -y

# Install Pi-hole
curl -sSL https://install.pi-hole.net | bash

# Install Unbound
sudo apt install unbound -y

# Install ad-skipper dependencies
pip3 install requests beautifulsoup4 tensorflow
