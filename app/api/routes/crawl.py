from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.db.deps import get_db
from app.domain.models.job import JobType
from app.domain.services.crawl_service import schedule_crawl
from app.api.schemas.job import CrawlAllResponse, JobResponse

router = APIRouter(prefix="/crawl", tags=["crawl"])


@router.post("/hockey", response_model=JobResponse)
async def crawl_hockey(db: Session = Depends(get_db)):
    job = await schedule_crawl(db, JobType.hockey)
    return {
        "job_id": job.id,
        "status_url": f"/jobs/{job.id}",
        "results_url": f"/jobs/{job.id}/results"
    }


@router.post("/oscar", response_model=JobResponse)
async def crawl_oscar(db: Session = Depends(get_db)):
    job = await schedule_crawl(db, JobType.oscar)
    return {
        "job_id": job.id,
        "status_url": f"/jobs/{job.id}",
        "results_url": f"/jobs/{job.id}/results"
    }


@router.post("/all", response_model=CrawlAllResponse)
async def crawl_all(db: Session = Depends(get_db)):
    hockey = await schedule_crawl(db, JobType.hockey)
    oscar = await schedule_crawl(db, JobType.oscar)

    return {
        "hockey_job_id": hockey.id,
        "hockey_status_url": f"/jobs/{hockey.id}",
        "hockey_results_url": f"/jobs/{hockey.id}/results",
        "oscar_job_id": oscar.id,
        "oscar_status_url": f"/jobs/{oscar.id}",
        "oscar_results_url": f"/jobs/{oscar.id}/results",
    }
