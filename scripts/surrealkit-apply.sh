#!/bin/sh
set -eu

TARGET="${1:-surreal}"

HOST="${SURREALDB_URL:-${SURREALKIT_HOST:-}}"
DB="${SURREALDB_DATABASE:-${SURREALKIT_DB:-}}"
NS="${SURREALDB_NAMESPACE:-${SURREALKIT_NS:-}}"
USER="${SURREALDB_USER:-${SURREALKIT_USER:-}}"
PASS="${SURREALDB_PASS:-${SURREALKIT_PASS:-}}"

if [ -z "$HOST" ] || [ -z "$DB" ] || [ -z "$NS" ] || [ -z "$USER" ] || [ -z "$PASS" ]; then
  cat <<'EOF' >&2
Missing SurrealDB connection environment variables.
Set SURREALDB_URL, SURREALDB_DATABASE, SURREALDB_NAMESPACE, SURREALDB_USER, and SURREALDB_PASS.
EOF
  exit 1
fi

exec surrealkit apply "$TARGET" \
  --host "$HOST" \
  --db "$DB" \
  --ns "$NS" \
  --user "$USER" \
  --pass "$PASS"
