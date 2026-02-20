from fastapi import FastAPI
from app.api.routes import health, crawl, jobs

app = FastAPI(title="RPA Crawler")

app.include_router(health.router)
app.include_router(crawl.router)
app.include_router(jobs.router)
