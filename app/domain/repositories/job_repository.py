from sqlalchemy.orm import Session

from app.domain.models.job import Job, JobType


def create_job(db: Session, job_type: JobType) -> Job:
    job = Job(type=job_type)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def list_jobs(db: Session):
    return db.query(Job).all()


def get_job(db: Session, job_id):
    return db.get(Job, job_id)
