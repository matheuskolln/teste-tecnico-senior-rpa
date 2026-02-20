from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.infrastructure.db.deps import get_db
from app.domain.repositories.job_repository import list_jobs, get_job, get_job_results

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/")
def get_all_jobs(db: Session = Depends(get_db)):
    return list_jobs(db)


@router.get("/{job_id}")
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    return get_job(db, job_id)


@router.get("/{job_id}/results")
def job_results(job_id: str, db: Session = Depends(get_db)):
    return get_job_results(db, job_id)
