from uuid import UUID
from pydantic import BaseModel


class JobResponse(BaseModel):
    job_id: UUID

class CrawlAllResponse(BaseModel):
    hockey_job_id: UUID
    oscar_job_id: UUID
