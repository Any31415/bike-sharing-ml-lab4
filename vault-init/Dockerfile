FROM python:3.11-slim

RUN pip install --no-cache-dir ansible-core

WORKDIR /app
COPY .env.vault .
COPY gdrive-credentials.json.vault .
COPY vault-init/decrypt.sh .
RUN sed -i 's/\r$//' decrypt.sh
RUN chmod +x decrypt.sh

ENTRYPOINT ["./decrypt.sh"]