from abc import ABC, abstractmethod
from typing import Iterable

from requests import Session

from utils import parse_cookies
from configs import configs
from models import WebsiteNames


class Parser(ABC):
    """Abstract class for jobs data parsing."""

    @abstractmethod
    def parse(self, session: Session) -> Iterable[dict]:
        pass


class AcademicworkParser(Parser):
    """Class for parsing jobs data from academicwork website."""

    def parse(self, session: Session) -> Iterable[dict]:
        req_data = configs[WebsiteNames.academicwork]
        response = session.post(
            req_data.get('base_url'),
            headers=req_data.get('headers', {}),
            json=req_data.get('body', {}),
            cookies=parse_cookies(req_data.get('raw_cookie', '')),
        )
        response.raise_for_status()

        for job_add in response.json()['Adverts']:
            yield {**job_add, 'website': WebsiteNames.academicwork}


class JobupParser(Parser):
    """Class for parsing jobs data from jobup website."""

    def parse(self, session: Session) -> Iterable[dict]:
        req_data = configs[WebsiteNames.jobup]
        response = session.get(
            req_data.get('base_url'), headers=req_data.get('headers', {})
        )
        response.raise_for_status()

        for job_add in response.json()['documents']:
            yield {**job_add, 'website': WebsiteNames.jobup}


def get_parser(website_name: WebsiteNames) -> Parser | None:
    return {
        WebsiteNames.academicwork: AcademicworkParser,
        WebsiteNames.jobup: JobupParser,
    }.get(website_name)()
