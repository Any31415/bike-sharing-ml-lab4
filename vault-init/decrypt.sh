#!/bin/sh
set -e

echo "$VAULT_PASSWORD" > /tmp/vp
chmod 600 /tmp/vp

ansible-vault decrypt .env.vault --output /secrets/.env --vault-password-file /tmp/vp
ansible-vault decrypt gdrive-credentials.json.vault --output /secrets/gdrive-credentials.json --vault-password-file /tmp/vp

rm /tmp/vp
echo "secrets decrypted into /secrets/"