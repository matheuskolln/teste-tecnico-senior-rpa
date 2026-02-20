from fastapi import FastAPI
from app.api.routes import health, crawl, jobs, truth_data

app = FastAPI(title="RPA Crawler")

app.include_router(health.router)
app.include_router(crawl.router)
app.include_router(jobs.router)
app.include_router(truth_data.router)
