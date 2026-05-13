#!/bin/bash
# AGenNext VPS Deployment Script
# Run as: sudo bash deploy.sh

set -e
echo "=== AGenNext Deployment ==="

# 1. Install Docker
echo "[1/5] Installing Docker..."
apt update && apt install -y docker.io docker-compose curl

# 2. Create app directory
echo "[2/5] Creating app directory..."
mkdir -p /app && cd /app

# 3. Copy files (run this from your local machine)
# scp -r ./agennext-ui user@vps.open-data.world:/app/
# scp server.py docker-compose.yml user@vps.open-data.world:/app/

# 4. Create environment file
echo "[3/5] Setting up environment..."
cat > .env <<EOF
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
REDIS_PASSWORD=$(openssl rand -base64 32)
EOF

# 5. Build and start
echo "[4/5] Building containers..."
docker compose build

echo "[5/5] Starting services..."
docker compose up -d

# Wait for health
echo "Waiting for services..."
sleep 10

# Check status
echo ""
echo "=== Deployment Complete ==="
docker compose ps
echo ""
echo "Frontend: http://$(hostname -I | awk '{print $1}'):3000"
echo "Backend:  http://$(hostname -I | awk '{print $1}'):8000"
echo "API Docs: http://$(hostname -I | awk '{print $1}'):8000/docs"