import requests as rq
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from . import crud
from app.schemas import ApiResponse, WebsiteNames, JobAddBase
from app.database import get_db


# Init router
router = APIRouter(prefix='/api/v1/job_adds', tags=['job_adds'])


@router.get('/', status_code=status.HTTP_200_OK)
async def get_jobs(
    skip: int = 0, limit: int = 20, db: Session = Depends(get_db)
) -> ApiResponse:
    _result = crud.get_all(db, skip, limit)
    return ApiResponse(
        code=status.HTTP_200_OK,
        status='Ok',
        message='Successfuly retrieved all job adds.',
        result=_result,
    ).dict(exclude_none=True)


@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_by_id(id: int, db: Session = Depends(get_db)) -> ApiResponse:
    """Get one job add by id route."""
    _result = crud.get_by_id(db, id)
    return ApiResponse(
        code=status.HTTP_200_OK,
        status='Ok',
        message='Successfuly retrieved job add.',
        result=_result,
    ).dict(exclude_none=True)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_job(job_add: JobAddBase, db: Session = Depends(get_db)):
    _inserted = crud.create(db, job_add)
    return ApiResponse(
        code=status.HTTP_201_CREATED,
        status='Created',
        message='Successfuly created new job add',
        result=_inserted,
    )


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(id: int, db: Session = Depends(get_db)) -> None:
    crud.remove(db, id)


@router.get('/scrape/{website}', status_code=status.HTTP_200_OK)
async def scrape_jobs(
    website: WebsiteNames, q: str | None = None, db: Session = Depends(get_db)
) -> ApiResponse:
    """Scraping endpoint"""
    result = crud.scrape_jobs(website)
    return ApiResponse(
        code=status.HTTP_200_OK,
        status='Ok',
        message=f'Successfuly scraped {website} job adds',
        result=result,
    ).dict(exclude_none=True)
