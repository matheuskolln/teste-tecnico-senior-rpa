from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.db.deps import get_db
from app.domain.models.job import JobType
from app.domain.services.crawl_service import schedule_crawl
from app.api.schemas.job import JobResponse

router = APIRouter(prefix="/crawl", tags=["crawl"])


@router.post("/hockey", response_model=JobResponse)
async def crawl_hockey(db: Session = Depends(get_db)):
    job = await schedule_crawl(db, JobType.hockey)
    return {"job_id": job.id}


@router.post("/oscar", response_model=JobResponse)
async def crawl_oscar(db: Session = Depends(get_db)):
    job = await schedule_crawl(db, JobType.oscar)
    return {"job_id": job.id}


@router.post("/all")
async def crawl_all(db: Session = Depends(get_db)):
    hockey = await schedule_crawl(db, JobType.hockey)
    oscar = await schedule_crawl(db, JobType.oscar)

    return {
        "hockey_job_id": hockey.id,
        "oscar_job_id": oscar.id,
    }
