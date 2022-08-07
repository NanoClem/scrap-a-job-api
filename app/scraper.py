import requests as rq

from models import WebsiteNames
from configs import configs
from parser import get_parser


class Scraper:
    def __init__(self) -> None:
        self.session = rq.Session()

    def scrape(self, website_name: WebsiteNames) -> list[dict]:
        """Scrap website to get jobs data."""
        with self.session as session:
            job_parser = get_parser(website_name)
            try:
                data = [job_data for job_data in job_parser.parse(session)]
            except rq.HTTPError as err:
                raise err

        return data
