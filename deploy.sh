#!/bin/bash
# One-command deployment from GitHub
# Run: curl -sL https://raw.githubusercontent.com/AGenNext/AgentGraph/feature/complete-platform/deploy.sh | bash

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[DEPLOY]${NC} $1"; }

log "Downloading AGenNext from GitHub..."

# Create app directory
mkdir -p /opt/agennext
cd /opt/agennext

# Download files from GitHub raw
log "Downloading frontend..."
curl -sLo frontend.tar.gz "https://raw.githubusercontent.com/AGenNext/AgentGraph/feature/complete-platform/agennext-ui.tar.gz" 2>/dev/null || \
curl -sL "https://github.com/AGenNext/AgentGraph/archive/feature/complete-platform.tar.gz" -o agentgraph.tar.gz

log "Downloading server..."
curl -sLo server.py "https://raw.githubusercontent.com/AGenNext/AgentGraph/feature/complete-platform/server.py"
curl -sLo docker-compose.yml "https://raw.githubusercontent.com/AGenNext/AgentGraph/feature/complete-platform/docker-compose.yml"

# Check if files exist
if [ -f server.py ]; then
    log "Files downloaded successfully"
    echo "Run: cd /opt/agennext && docker compose up -d"
else
    echo "Manual download required"
    echo "git clone -b feature/complete-platform https://github.com/AGenNext/AgentGraph.git /opt/agennext"
fi