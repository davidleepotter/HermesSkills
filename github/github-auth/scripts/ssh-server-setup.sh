#!/usr/bin/env bash
# SSH server setup script for remote access to Linux machines
# Usage: ./ssh-server-setup.sh

set -e

echo "Installing OpenSSH server..."
sudo apt update
sudo apt install -y openssh-server

echo "Starting and enabling SSH service..."
sudo systemctl start ssh
sudo systemctl enable ssh

echo "Configuring firewall (if ufw is active)..."
if command -v ufw &>/dev/null && sudo ufw status | grep -q "Status: active"; then
    sudo ufw allow OpenSSH
fi

echo "SSH server setup complete!"
echo ""
echo "To connect from another machine:"
echo "  ssh <username>@<this-machine-ip>"
echo ""
echo "Your IP address: $(hostname -I | awk '{print $1}')"
