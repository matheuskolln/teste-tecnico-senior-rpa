import json
import asyncio
import aio_pika

from app.core.config import settings
from app.infrastructure.db.session import SessionLocal
from app.domain.repositories.job_repository import update_job_status
from app.domain.models.job import JobStatus

from app.infrastructure.scrapers.hockey import scrape_hockey
from app.infrastructure.scrapers.oscar import scrape_oscar


SCRAPER_MAP = {
    "hockey": scrape_hockey,
    "oscar": scrape_oscar,
}


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body)

        job_id = data["job_id"]
        job_type = data["type"]

        db = SessionLocal()

        try:
            print(f"Processing job {job_id} ({job_type})")

            update_job_status(db, job_id, JobStatus.running)

            scraper = SCRAPER_MAP.get(job_type)
            if scraper is None:
                raise ValueError(f"Unknown job type: {job_type}")
            result = await scraper()
            print("Result:", len(result))

            update_job_status(db, job_id, JobStatus.completed)

        except Exception as e:
            print("Worker error:", e)
            update_job_status(db, job_id, JobStatus.failed)

        finally:
            db.close()


async def connect_with_retry(url, retries=20, delay=3):
    for i in range(retries):
        try:
            print("Connecting to RabbitMQ...")
            return await aio_pika.connect_robust(url)
        except Exception:
            print(f"RabbitMQ not ready — retry {i+1}/{retries}")
            await asyncio.sleep(delay)

    raise RuntimeError("Could not connect to RabbitMQ")


async def main():
    connection = await connect_with_retry(settings.rabbitmq_url)

    channel = await connection.channel()

    hockey_queue = await channel.declare_queue("hockey_queue", durable=True)
    oscar_queue = await channel.declare_queue("oscar_queue", durable=True)

    await hockey_queue.consume(process_message)
    await oscar_queue.consume(process_message)

    print("Worker running...")
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
