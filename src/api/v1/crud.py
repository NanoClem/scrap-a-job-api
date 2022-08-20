import requests as rq
import sqlalchemy.orm as sql_orm
from fastapi import HTTPException, status

from api import schemas, models
from api.scraping.scrapers import get_scraper


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
    return new_job


def remove(db: sql_orm.Session, job_id: int):
    """Delete one job add from database."""
    _job_add = get_by_id(db, job_id)
    db.delete(_job_add)
    db.commit()


def scrape(db: sql_orm.Session, website_name: schemas.WebsiteNames) -> list[dict]:
    """Scrap job adds data from given website."""
    job_scraper = get_scraper(website_name)
    with rq.Session() as rq_session:
        try:
            db_jobs = [
                models.JobModel(**job_data.dict())
                for job_data in job_scraper.scrape(rq_session)
            ]
        except rq.HTTPError as err:
            raise err

    # Save to database
    db.bulk_save_objects(db_jobs)
    db.commit()

    return db_jobs
