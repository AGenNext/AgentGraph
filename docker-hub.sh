#!/bin/bash
# Docker Build & Push to Docker Hub

set -e

# =========================================================================
# Configuration
# =========================================================================

DOCKER_HUB_USERNAME=${DOCKER_HUB_USERNAME:-}
DOCKER_HUB_PASSWORD=${DOCKER_HUB_PASSWORD:-}
IMAGE_NAME=${IMAGE_NAME:-agennext/enterprise}
IMAGE_TAG=${IMAGE_TAG:-latest}

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# =========================================================================
# Functions
# =========================================================================

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# =========================================================================
# Docker Build
# =========================================================================

build() {
    log_info "Building Docker image..."
    
    docker build \
        --tag ${IMAGE_NAME}:${IMAGE_TAG} \
        --tag ${IMAGE_NAME}:latest \
        .
    
    log_info "Build complete: ${IMAGE_NAME}:${IMAGE_TAG}"
}

# =========================================================================
# Docker Login
# =========================================================================

login() {
    if [ -z "$DOCKER_HUB_USERNAME" ] || [ -z "$DOCKER_HUB_PASSWORD" ]; then
        log_warn "Docker Hub credentials not set, skipping login"
        return 1
    fi
    
    log_info "Logging into Docker Hub..."
    echo "$DOCKER_HUB_PASSWORD" | docker login -u "$DOCKER_HUB_USERNAME" --password-stdin
    log_info "Login successful"
}

# =========================================================================
# Docker Push
# =========================================================================

push() {
    log_info "Pushing to Docker Hub..."
    
    docker push ${IMAGE_NAME}:${IMAGE_TAG}
    docker push ${IMAGE_NAME}:latest
    
    log_info "Push complete: ${IMAGE_NAME}:${IMAGE_TAG}"
}

# =========================================================================
# Docker Pull
# =========================================================================

pull() {
    log_info "Pulling from Docker Hub..."
    
    docker pull ${IMAGE_NAME}:${IMAGE_TAG}
    docker pull ${IMAGE_NAME}:latest
    
    log_info "Pull complete"
}

# =========================================================================
# Build & Push All-in-One
# =========================================================================

build_and_push() {
    # Build
    docker build \
        --tag ${IMAGE_NAME}:${IMAGE_TAG} \
        --tag ${IMAGE_NAME}:latest \
        .
    
    # Login
    if [ -n "$DOCKER_HUB_USERNAME" ] && [ -n "$DOCKER_HUB_PASSWORD" ]; then
        echo "$DOCKER_HUB_PASSWORD" | docker login -u "$DOCKER_HUB_USERNAME" --password-stdin
    fi
    
    # Push
    docker push ${IMAGE_NAME}:${IMAGE_TAG}
    docker push ${IMAGE_NAME}:latest
    
    log_info "Build & Push complete!"
}

# =========================================================================
# Multi-Architecture Build
# =========================================================================

build_manifest() {
    log_info "Building multi-architecture manifest..."
    
    # Build for multiple architectures
    docker buildx build \
        --platform linux/amd64,linux/arm64 \
        --tag ${IMAGE_NAME}:${IMAGE_TAG} \
        --tag ${IMAGE_NAME}:latest \
        --push .
    
    log_info "Multi-arch build complete"
}

# =========================================================================
# Main
# =========================================================================

case "${1:-build}" in
    build)
        build
        ;;
    push)
        if [ -n "$DOCKER_HUB_USERNAME" ] && [ -n "$DOCKER_HUB_PASSWORD" ]; then
            build_and_push
        else
            log_error "DOCKER_HUB_USERNAME and DOCKER_HUB_PASSWORD required"
            exit 1
        fi
        ;;
    pull)
        pull
        ;;
    login)
        login
        ;;
    manifest)
        build_manifest
        ;;
    *)
        echo "Usage: $0 {build|push|pull|login|manifest}"
        exit 1
        ;;
esac

# =========================================================================
# Environment Variables for CI/CD
# =========================================================================

"""
Environment Variables:
- DOCKER_HUB_USERNAME: Docker Hub username
- DOCKER_HUB_PASSWORD: Docker Hub password/token
- IMAGE_NAME: Image name (default: agennext/enterprise)
- IMAGE_TAG: Image tag (default: latest)

Usage:
  DOCKER_HUB_USERNAME=user DOCKER_HUB_PASSWORD=token ./docker-hub.sh push
  
  # Or with custom image
  IMAGE_NAME=myorg/agent IMAGE_TAG=v1.0 ./docker-hub.sh push
"""

# =========================================================================
# GitHub Actions Example
# =========================================================================

"""
name: Docker Build and Push

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: \${{ secrets.DOCKER_HUB_USERNAME }}
          password: \${{ secrets.DOCKER_HUB_PASSWORD }}
          
      - name: Build and push
        run: |
          docker build -t agennext/enterprise:latest .
          docker push agennext/enterprise:latest
"""