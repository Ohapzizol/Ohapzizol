import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from app.db.session import db_engine
from app.db.base import Base


def create_tables():
    Base.metadata.create_all(bind=db_engine)


def get_application():
    create_tables()
    return FastAPI()


logging.basicConfig(level='INFO')

app = get_application()

scheduler = AsyncIOScheduler(daemon=True, timezone='Asia/Seoul')

