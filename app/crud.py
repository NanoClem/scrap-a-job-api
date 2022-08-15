import requests as rq
import sqlalchemy.orm as sql_orm

from . import models, schemas
from .scrapers import get_scraper


def get_job(db: sql_orm.Session, job_id: int):
    return db.query(models.JobModel).filter(models.JobModel.id == job_id).first()


def get_jobs(db: sql_orm.Session, skip: int = 0, limit: int = 100):
    return db.query(models.JobModel).offset(skip).limit(limit).all()


def scrape_jobs(db: sql_orm.Session, website_name: schemas.WebsiteNames) -> list[dict]:
    """Scrap given website to get jobs data."""
    # Make scraping requests
    with rq.Session() as rq_session:
        job_parser = get_scraper(website_name)
        try:
            db_jobs = [
                models.JobModel(**job_data)
                for job_data in job_parser.scrape(rq_session)
            ]
        except rq.HTTPError as err:
            raise err

    # Save to database
    db.bulk_save_objects(db_jobs)
    db.commit()

    return db_jobs
