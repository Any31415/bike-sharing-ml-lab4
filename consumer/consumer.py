from kafka import KafkaConsumer
import json
from src.db import save_prediction  # переиспользуешь свою же функцию

consumer = KafkaConsumer(
    "predictions",
    bootstrap_servers="kafka:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",
)

for message in consumer:
    record = message.value
    save_prediction(record["input"], record["result"])
    print(f"Saved: {record}")