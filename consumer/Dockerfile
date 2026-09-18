FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt kafka-python
COPY src/ ./src/
COPY consumer/consumer.py .
COPY consumer/entrypoint.sh .
RUN sed -i 's/\r$//' entrypoint.sh
RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]