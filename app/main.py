import requests as rq
from fastapi import FastAPI, HTTPException, status

from . import crud
from .schemas import WebsiteNames


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "planet"}


@app.get("/jobs/scrape/{website}", status_code=status.HTTP_200_OK)
async def scrape_jobs(website: WebsiteNames, q: str | None = None):
    """d"""
    try:
        result = crud.scrape_jobs(website)
    except rq.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='An error occured while scraping data.',
        )
    return result
