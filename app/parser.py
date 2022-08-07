from abc import ABC, abstractmethod
from typing import ClassVar, Iterable

from requests import Session, Response

from utils import parse_cookies
from configs import configs
from models import WebsiteNames


class Parser(ABC):
    """Abstract class for jobs data parsing."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the parser"""

    @property
    @abstractmethod
    def req_data(self) -> dict:
        """Data used to make the request."""

    @abstractmethod
    def _make_request(self, session: Session) -> Response:
        """Make a request"""

    @abstractmethod
    def parse(self, session: Session) -> Iterable[dict]:
        """Parse data obtained from a request."""


class AcademicworkParser(Parser):
    """Class for parsing jobs data from academicwork website."""

    name: ClassVar[str] = WebsiteNames.academicwork
    req_data: ClassVar[dict] = configs[name]

    def _make_request(self, session: Session) -> Response:
        response = session.post(
            self.req_data.get('base_url'),
            headers=self.req_data.get('headers', {}),
            json=self.req_data.get('body', {}),
            cookies=parse_cookies(self.req_data.get('raw_cookie', '')),
        )
        response.raise_for_status()
        return response

    def parse(self, session: Session) -> Iterable[dict]:
        res = self._make_request(session)
        for job_add in res.json()['Adverts']:
            yield {**job_add, 'website': self.name}


class JobupParser(Parser):
    """Class for parsing jobs data from jobup website."""

    name: ClassVar[str] = WebsiteNames.jobup
    req_data: ClassVar[dict] = configs[name]

    def _make_request(self, session: Session) -> Response:
        response = session.get(
            self.req_data.get('base_url'), headers=self.req_data.get('headers', {})
        )
        response.raise_for_status()
        return response

    def parse(self, session: Session) -> Iterable[dict]:
        res = self._make_request(session)
        for job_add in res.json()['documents']:
            yield {**job_add, 'website': self.name}


def get_parser(website_name: WebsiteNames) -> Parser | None:
    return {
        WebsiteNames.academicwork: AcademicworkParser,
        WebsiteNames.jobup: JobupParser,
    }.get(website_name)()
