from typing import Iterable
import sqlalchemy.orm as sql_orm

from api import schemas, models


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


def create_many(db: sql_orm.Session, job_adds: Iterable[schemas.JobAddBase]):
    """Bulk creation of jobs in database."""
    _new_jobs = []
    for job_add in job_adds:
        db_jd = get_by_source_id(db, job_add.source_id)
        if db_jd is None:
            inserted_job = create(db, job_add)
            _new_jobs.append(inserted_job)

    return _new_jobs


def remove(db: sql_orm.Session, job_id: int):
    """Delete one job add from database."""
    _job_add = get_by_id(db, job_id)
    db.delete(_job_add)
    db.commit()
