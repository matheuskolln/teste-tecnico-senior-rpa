import json
import aio_pika

from app.core.config import settings


async def publish_message(queue_name: str, payload: dict):
    connection = await aio_pika.connect_robust(
        settings.rabbitmq_url,
        timeout=5
    )

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue(queue_name, durable=True)

        message = aio_pika.Message(
            body=json.dumps(payload).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await channel.default_exchange.publish(message, routing_key=queue.name)
