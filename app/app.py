import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.db.base import Base
from app.db.session import db_engine


def create_tables():
    Base.metadata.create_all(bind=db_engine)


def get_application():
    create_tables()
    return FastAPI()


logging.basicConfig(level='INFO')

app = get_application()

scheduler = AsyncIOScheduler(daemon=True, timezone='Asia/Seoul')

