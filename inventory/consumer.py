import asyncio
from json import loads

import aiojobs
from aiokafka import AIOKafkaConsumer
from inventory.consumer_handler.performers import *
from inventory.consumer_handler.handler import event_handler


async def consume_be():
    consumer = AIOKafkaConsumer(
        "accounts",
        bootstrap_servers="broker:9092",
        group_id="my-group",
        value_deserializer=lambda x: loads(x.decode("utf-8")),
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        print("Run consumer for business events")
        # Consume messages
        async for msg in consumer:
            print(
                "consumed: ",
                msg.topic,
                msg.partition,
                msg.offset,
                msg.key,
                msg.value,
                msg.timestamp,
            )
    except asyncio.exceptions.CancelledError:
        print("Business events consumer: Good bye!")
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


async def consume_cud():
    consumer = AIOKafkaConsumer(
        "accounts-stream",
        bootstrap_servers="broker:9092",
        group_id="my-group",
        value_deserializer=lambda x: loads(x.decode("utf-8")),
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        print("Run consumer for CUD events")
        # Consume messages
        async for msg in consumer:
            print(
                "consumed: ",
                msg.topic,
                msg.partition,
                msg.offset,
                msg.key,
                msg.value,
                msg.timestamp,
            )
            event_handler.process_event(Event(**msg.value))
    except asyncio.exceptions.CancelledError:
        print("CUD events consumer: Good bye!")
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


async def main():
    scheduler = await aiojobs.create_scheduler()

    await scheduler.spawn(consume_be())
    await scheduler.spawn(consume_cud())

    return scheduler


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    print("Run event consumers")

    try:
        scheduler = loop.run_until_complete(main())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(scheduler.close())
