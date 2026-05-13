#!/bin/bash
# VPS Deploy Script for Ubuntu
# Run: bash vps-deploy.sh

set -e

VPS_HOST="${1:-root@vps.open-data.world}"
APP_DIR="/opt/agennext"

echo "=== Deploying to $VPS_HOST ==="

# SSH and deploy
ssh $VPS_HOST << 'EOF'
set -e

# Update and install Docker
apt-get update -y
apt-get install -y docker.io docker-compose

# Create app directory
mkdir -p /opt/agennext
cd /opt/agennext

# Clone from GitHub
git clone -b feature/complete-platform https://github.com/AGenNext/AgentGraph.git .

# Build and start
docker compose up -d --build

echo "=== Deployed ==="
curl -s localhost:8000/health
EOF

echo "=== Done ==="
