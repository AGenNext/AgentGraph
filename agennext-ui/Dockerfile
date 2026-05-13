# AGenNext Enterprise - Production-Grade Dockerfile
# Multi-stage build with security hardening

# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first for dependency caching
COPY package.json package-lock.json* ./

# Install dependencies with strict audit
RUN npm ci --legacy-peer-deps --audit --fund && \
    npm cache clean --force

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Remove dev dependencies from production
RUN npm prune --production

# Stage 2: Production - Hardened
FROM node:20-alpine AS runner

WORKDIR /app

# === SECURITY: Create non-root user ===
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# === SECURITY: Install security tools ===
RUN apk add --no-cache \
    dumb-init \
    curl \
    tzdata \
    && chown -R nextjs:nodejs /app

# === ENVIRONMENT ===
ENV NODE_ENV=production \
    PORT=3000 \
    HELKHEALTHINTERVAL=30s \
    HELKHEALTHTIMEOUT=3s \
    HELKHEALTHSTARTPERIOD=5s \
    HELKHEALTHRETRIES=3

# Copy built artifacts from builder
COPY --chown=nextjs:nodejs --from=builder /app/package.json ./package.json
COPY --chown=nextjs:nodejs --from=builder /app/package-lock.json* ./
COPY --chown=nextjs:nodejs --from=builder /app/.next ./.next
COPY --chown=nextjs:nodejs --from=builder /app/public ./public
COPY --chown=nextjs:nodejs --from=builder /app/.env.production.template ./.env.production

# === SECURITY: Set proper permissions ===
RUN mkdir -p /app/.next/cache /app/tmp && \
    chown -R nextjs:nodejs /app && \
    chmod 755 /app/public

# === SECURITY: Switch to non-root user ===
USER nextjs

# Expose port
EXPOSE 3000

# === HEALTH CHECK ===
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# === STARTUP ===
# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Run as non-root user
CMD ["node", "server.js"]

# === SECURITY NOTES ===
# - Runs as non-root user (nextjs:1001)
# - No secrets in image (use env vars or secrets manager)
# - Health endpoint for container orchestration
# - Production dependencies only
# - Immutable starting point