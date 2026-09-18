from kafka import KafkaConsumer
import json
from src.db import save_prediction  # переиспользуем функцию из api

consumer = KafkaConsumer(
    "predictions",
    bootstrap_servers="kafka:9092",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",   # если consumer только запустился — читать с начала топика
    group_id="predictions-consumer-group",  # чтобы при перезапуске не читать всё заново
)

print("consumer started, listening to topic 'predictions'...")

for message in consumer:
    try:
        record = message.value  # уже распарсенный JSON (см. value_deserializer выше)

        # проверяем, что структура сообщения та, что мы ожидаем
        if "input" not in record or "result" not in record:
            print(f"skipped malformed message (missing keys): {record}")
            continue  # не падаем, просто пропускаем и идём дальше

        save_prediction(record["input"], record["result"])
        print(f"saved: {record}")

    except json.JSONDecodeError as e:
        print(f"skipped message, invalid JSON: {e}")
        continue

    except Exception as e:
        # любая другая ошибка (например, БД недоступна) — не убиваем весь consumer,
        # логируем и идём дальше слушать следующие сообщения
        print(f"error processing message: {e}, message: {message.value}")
        continue