from sqlalchemy import create_engine

from app.core.config import config


def get_engine():
    return create_engine(config.DATABASE_DSN, echo=True)
