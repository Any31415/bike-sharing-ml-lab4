#!/bin/sh
set -e

echo "waiting for secrets from vault-init..."
while [ ! -f /secrets/.env ]; do
  sleep 1
done

set -a
. /secrets/.env
set +a

exec python consumer.py