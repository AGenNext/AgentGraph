# VPS Deployment Guide for vps.open-data.world

## Current Status
- VPS IP: 144.217.12.160
- Port 80: Returns 404 (something running)
- Ports 3000/8000: Not exposed

## How to Deploy

### Option 1: Docker (Recommended)

```bash
# SSH to VPS
ssh root@vps.open-data.world

# Or from local terminal:
# scp -r ./agennext-ui root@vps.open-data.world:/app/
# scp server.py docker-compose.yml root@vps.open-data.world:/app/
```

### Option 2: Manual Install

```bash
# SSH into VPS
ssh user@144.217.12.160

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

# Install Python
apt install -y python3 python3-pip

# Clone/Copy your project
cd /var/www
# Copy your agennext-ui folder here

# Install and start
cd agennext-ui
npm install
npm run build
npm run start &

# Start backend
cd ..
python3 -m pip install fastapi uvicorn
python3 server.py &
```

### Option 3: Docker Compose (if Docker available on VPS)

```bash
# On VPS
apt install docker.io
systemctl start docker

cd /app
docker compose up -d
```

## Files Ready to Deploy
- /workspace/project/agennext-ui/ (Next.js frontend)
- /workspace/project/server.py (FastAPI backend)
- /workspace/project/docker-compose.yml (Production config)