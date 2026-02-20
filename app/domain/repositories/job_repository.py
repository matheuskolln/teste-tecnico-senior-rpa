from app.domain.models.job_result import JobResult
from sqlalchemy.orm import Session

from app.domain.models.job import Job, JobType, JobStatus


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

def update_job_status(db: Session, job_id: str, status: JobStatus):
    job = db.get(Job, job_id)

    if not job:
        raise ValueError(f"Job {job_id} not found")

    job.status = status
    db.commit()
    db.refresh(job)

    return job

def create_job_result(db: Session, job_id: str, data: dict):
    result = JobResult(job_id=job_id, data=data)
    db.add(result)
    db.commit()

def get_job_results(db: Session, job_id: str):
    return db.query(JobResult).filter(JobResult.job_id == job_id).first()
