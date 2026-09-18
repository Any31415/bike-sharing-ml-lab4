#!/bin/sh
set -e

echo "waiting for secrets from vault-init..."
while [ ! -f /secrets/.env ]; do
  sleep 1
done

set -a
. /secrets/.env
set +a

echo "pulling model via dvc..."
export GDRIVE_CREDENTIALS_DATA="$(cat /secrets/gdrive-credentials.json)"
dvc pull models/model.pkl.dvc

exec uvicorn src.api:app --host 0.0.0.0 --port 8000