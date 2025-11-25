from pydantic import BaseSettings

class Settings(BaseSettings):
    app_env: str = "development"
    secret_key: str
    database_url: str
    redis_host: str = "redis"
    redis_port: int = 6379
    celery_broker_url: str
    celery_result_backend: str
    chroma_persist_dir: str = "/data/chroma"

    class Config:
        env_file = ".env"

settings = Settings()
