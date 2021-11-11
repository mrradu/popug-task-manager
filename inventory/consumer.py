import asyncio
import os
import signal
from json import loads

import aiojobs
from aiokafka import AIOKafkaConsumer
from kafka.errors import KafkaConnectionError
from loguru import logger

from inventory.consumer_handler.performers import *


def attach_consumer(topic: str, group_id: str = 'my-group'):
    def wrapper(f):
        async def wrapped(host: str, *args, port: int = 9092, **kwargs):
            consumer = AIOKafkaConsumer(
                topic,
                bootstrap_servers=f"{host}:{port}",
                group_id=group_id,
                value_deserializer=lambda x: loads(x.decode("utf-8")),
            )

            while True:
                try:
                    await consumer.start()
                    break
                except KafkaConnectionError:
                    await asyncio.sleep(5)

            try:
                logger.info(f"Run event consumer for topic `{topic}`")
                await f(consumer, *args, **kwargs)
            except asyncio.exceptions.CancelledError:
                logger.info(f'Shutdown event consumer for topic `{topic}`')
            finally:
                await consumer.stop()

        return wrapped
    return wrapper


@attach_consumer('accounts')
async def consume_be(consumer: AIOKafkaConsumer):
    async for msg in consumer:
        logger.info(f"Consume event from topic `{msg.topic}`: {msg.value}")


@attach_consumer('accounts-stream')
async def consume_cud(consumer: AIOKafkaConsumer):
    async for msg in consumer:
        logger.info(f"Consume event from topic `{msg.topic}`: {msg.value}")


async def main():
    scheduler = await aiojobs.create_scheduler()

    host = os.environ.get('BROKER_HOST', 'localhost')

    await scheduler.spawn(consume_be(host=host))
    await scheduler.spawn(consume_cud(host=host))

    return scheduler


async def shutdown(scheduler, loop):
    await scheduler.close()
    loop.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    logger.info(f"Run event consumers")

    try:
        scheduler = loop.run_until_complete(main())

        signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
        for s in signals:
            loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(scheduler, loop)))

        loop.run_forever()
    finally:
        logger.info(f"Shutdown event consumers")
        loop.close()
