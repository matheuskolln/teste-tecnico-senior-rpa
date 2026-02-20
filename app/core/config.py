from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "rpa-crawler"
    database_url: str = "postgresql://postgres:postgres@db:5432/app"
    rabbitmq_url: str = "amqp://guest:guest@rabbitmq/"

    class Config:
        env_file = ".env"


settings = Settings()
