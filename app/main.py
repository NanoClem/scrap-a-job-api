import uvicorn
import requests as rq
from fastapi import FastAPI, HTTPException, status

from models import WebsiteNames
from scraper import Scraper


app = FastAPI()
scraper = Scraper()


@app.get("/")
async def read_root():
    return {"Hello": "planet"}


@app.get("/jobs/scrape/{website}", status_code=status.HTTP_200_OK)
async def scrape_jobs(website: WebsiteNames, q: str | None = None):
    """d"""
    try:
        result = scraper.scrape(website)
    except rq.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='An error occured while scraping data.',
        )
    return result


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=5000, reload=True)
