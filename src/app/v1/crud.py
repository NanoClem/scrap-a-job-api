import requests as rq
import sqlalchemy.orm as sql_orm
from fastapi import HTTPException, status

from app import schemas, models
from app.scraping.scrapers import get_scraper


def get_all(db: sql_orm.Session, skip: int = 0, limit: int = 100):
    """Get all job add in database with a limit and skip index."""
    return db.query(models.JobModel).offset(skip).limit(limit).all()


def get_by_id(db: sql_orm.Session, job_id: int):
    """Get a job add by its id"""
    _job_add = db.query(models.JobModel).filter_by(id=job_id).scalar()

    if _job_add is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Job add with id {id} not found.',
        )

    return _job_add


def create(db: sql_orm.Session, job_add: schemas.JobAddBase):
    """Create new job add in database."""
    _job_add = db.query(models.JobModel).filter_by(source_id=job_add.source_id).scalar()

    if _job_add is not None:  # Consider using put in the future
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Job add with source id {job_add.source_id} already exists',
        )

    new_job = models.JobModel(**job_add.dict())
    db.add(new_job)
    db.commit()

    return new_job


def remove(db: sql_orm.Session, id: int):
    """Delete one job add from database."""
    _job_add = get_by_id(db, id)

    if _job_add is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Job add with id {id} not found',
        )

    db.delete(_job_add)
    db.commit()


def scrape(db: sql_orm.Session, website_name: schemas.WebsiteNames) -> list[dict]:
    """Scrap job adds data from given website."""
    with rq.Session() as rq_session:
        job_parser = get_scraper(website_name)
        try:
            db_jobs = [
                models.JobModel(**job_data.dict())
                for job_data in job_parser.scrape(rq_session)
            ]
        except rq.HTTPError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'An error occured while scraping data from website {website_name}.',
            )

    # Save to database
    db.bulk_save_objects(db_jobs)
    db.commit()

    return db_jobs
