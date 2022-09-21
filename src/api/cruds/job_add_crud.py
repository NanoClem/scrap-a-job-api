from typing import Iterable

import httpx
import sqlalchemy.orm as sql_orm

from ..scraping.scrapers import get_scraper
from ..schemas.website_names import WebsiteNames
from ..schemas import job_add as schemas
from .. import models


def get_all(db: sql_orm.Session, skip: int = 0, limit: int = 100):
    """Get all job add in database with a limit and skip index."""
    return db.query(models.JobModel).offset(skip).limit(limit).all()


def get_by_id(db: sql_orm.Session, job_id: int):
    """Get a job add by its id"""
    return db.query(models.JobModel).filter_by(id=job_id).scalar()


def get_by_source_id(db: sql_orm.Session, source_id: str):
    """Get a job add by its source id"""
    return db.query(models.JobModel).filter_by(source_id=source_id).scalar()


def create(db: sql_orm.Session, job_add: schemas.JobAddBase):
    """Create new job add in database."""
    new_job = models.JobModel(**job_add.dict())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


def create_many(
    db: sql_orm.Session,
    job_adds: Iterable[schemas.JobAddBase],
    include_duplicates: bool = False,
):
    """Bulk creation of jobs in database."""
    _new_jobs = []
    for job_add in job_adds:
        db_jd = get_by_source_id(db, job_add.source_id)

        if db_jd is None:
            inserted_job = create(db, job_add)
            _new_jobs.append(inserted_job)
        elif include_duplicates:
            _new_jobs.append(db_jd)

    return _new_jobs


def remove(db: sql_orm.Session, job_id: int):
    """Delete one job add from database."""
    _job_add = get_by_id(db, job_id)
    db.delete(_job_add)
    db.commit()


async def scrape(db: sql_orm.Session, website_name: WebsiteNames, max_pages: int = 1):
    """d"""
    _results = []
    job_scraper = get_scraper(website_name)

    async with httpx.AsyncClient() as client:
        await job_scraper.scrape(client, _results, max_page=max_pages)

    return create_many(db, _results, include_duplicates=True)
