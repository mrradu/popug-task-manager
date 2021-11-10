import json

from loguru import logger
from kafka import KafkaProducer, KafkaConsumer


class Producer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers="broker:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def call(self, event, topic):
        logger.info(f"Send event with data {event} in topic: {topic}")
        res = self.producer.send(topic, event)
        logger.info(f"Res: {res}")
