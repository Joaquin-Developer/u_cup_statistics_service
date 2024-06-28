from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_DSN: str

    class Config:
        env_file = ".env"


config = Config()
