#!/bin/bash
# AGenNext VPS Auto-Deployer
# Run this ON your VPS after SSH login
# Usage: curl -s https://raw.githubusercontent.com/YOUR_REPO/main/deploy-auto.sh | bash

set -e

echo "=========================================="
echo "  AGenNext VPS Auto-Deployer"
echo "=========================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check if root
if [ "$EUID" -ne 0 ]; then
  log_error "Please run as root: sudo bash $0"
  exit 1
fi

log_info "Starting deployment..."

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VER=$VERSION_ID
fi
log_info "Detected: $OS $VER"

# Install Docker
log_info "Installing Docker..."
apt update -qq
apt install -y -qq docker.io docker-compose-plugin curl git wget

# Start Docker
systemctl start docker || true
systemctl enable docker || true

# Get server IP
SERVER_IP=$(hostname -I | awk '{print $1}')
log_info "Server IP: $SERVER_IP"

# Create app directory
APP_DIR="/opt/agennext"
mkdir -p $APP_DIR
cd $APP_DIR

log_info "Docker installed. Ready for deployment."
echo ""
echo "=========================================="
echo "  Next Steps:"
echo "=========================================="
echo "1. Copy your project files to $APP_DIR"
echo "2. Run: cd $APP_DIR && docker compose up -d"
echo ""
echo "Or manually install:"
echo "  apt install -y nodejs npm python3-pip"
echo "  cd agennext-ui && npm install && npm run build"
echo "  cd .. && pip install fastapi uvicorn"
echo "  python3 server.py &"
echo "=========================================="