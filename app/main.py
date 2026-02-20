from fastapi import FastAPI

from app.api.routes import health

app = FastAPI(title="RPA Crawler")

app.include_router(health.router)
