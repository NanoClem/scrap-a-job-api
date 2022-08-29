import requests as rq
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from api.database import get_db
from api.cruds import job_add_crud as crud
from api.schemas.job_add_schemas import JobAdd, JobAddBase
from api.schemas.website_names import WebsiteNames
from api.scraping.scrapers import get_scraper


# Init router
router = APIRouter(prefix='/api/job_adds', tags=['job_adds'])


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[JobAdd])
async def get_jobs(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Get all jobs stored in db. Can be paginated with skip and limit."""
    return crud.get_all(db, skip, limit)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=JobAdd)
async def get_by_id(id: int, db: Session = Depends(get_db)):
    """Get one job add by id route."""
    _result = crud.get_by_id(db, id)
    if _result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Job add with id {id} not found.',
        )
    return _result


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=JobAdd)
async def create_job(job_add: JobAddBase, db: Session = Depends(get_db)):
    """Create one job add."""
    db_job_add = crud.get_by_source_id(db, job_add.source_id)
    if db_job_add is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Job add with source id {job_add.source_id} already exists',
        )
    return crud.create(db, job_add)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(id: int, db: Session = Depends(get_db)):
    """Delete one job add."""
    # Check if already exists in db
    db_job_add = crud.get_by_id(db, id)
    if db_job_add is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Job add with id {id} not found',
        )
    crud.remove(db, id)


@router.get(
    '/scrape/{website}/last',
    status_code=status.HTTP_200_OK,
    response_model=list[JobAdd],
)
async def scrape_jobs(website: WebsiteNames, db: Session = Depends(get_db)):
    """Scrape and save most recent job adds from a supported website.\n
    Scrape only from the first page.
    Returned result includes only scraped job adds which are not already in db.
    """
    job_scraper = get_scraper(website)
    try:
        with rq.Session() as rq_session:
            _scraped_adds = (scraped for scraped in job_scraper.scrape(rq_session))
    except rq.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An error occured while scraping data from website {website}.',
        )

    return crud.create_many(db, _scraped_adds)
