from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "rpa-crawler"
    database_url: str
    rabbitmq_url: str

    class Config:
        env_file = ".env"


settings = Settings()
