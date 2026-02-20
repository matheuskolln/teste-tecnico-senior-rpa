from sqlalchemy.orm import Session

from app.domain.models.job import JobType
from app.domain.repositories.job_repository import create_job
from app.infrastructure.messaging.rabbitmq import publish_message


async def schedule_crawl(db: Session, job_type: JobType):
    job = create_job(db, job_type)

    await publish_message(
        queue_name=f"{job_type.value}_queue",
        payload={
            "job_id": str(job.id),
            "type": job_type.value,
        },
    )

    return job
