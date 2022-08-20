from abc import ABC, abstractmethod
from typing import ClassVar, Iterable

from requests import Session, Response

from api.schemas import WebsiteNames, JobAddBase
from .utils import parse_cookies
from .configs import configs


class Scraper(ABC):
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
    def _parse(self, raw_data: dict) -> JobAddBase:
        """Parse raw data into data schemas class."""

    @abstractmethod
    def scrape(self, session: Session) -> Iterable[JobAddBase]:
        """Scrape and parse data obtained from a request."""


class AcademicworkScraper(Scraper):
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

    def _parse(self, raw_data: dict) -> JobAddBase:
        return JobAddBase(
            source_id=str(raw_data.get('Id')),
            title=raw_data.get('JobTitle'),
            slug=raw_data.get('Slug'),
            url=f'https://jobs.academicwork.ch/job-list/{raw_data.get("Slug")}/{raw_data.get("Id")}',
            source_website=self.name,
            employment_type=raw_data.get('OrderType'),
            category=raw_data.get('Category'),
            extent=raw_data.get('WorkExtent'),
            description=raw_data.get('LeadIn'),
            location=raw_data.get('Location'),
            publication_date=raw_data.get('CreatedDate'),
        )

    def scrape(self, session: Session) -> Iterable[JobAddBase]:
        res = self._make_request(session)
        for job_add in res.json()['Adverts']:
            yield self._parse(job_add)


class JobupScraper(Scraper):
    """Class for parsing jobs data from jobup website."""

    name: ClassVar[str] = WebsiteNames.jobup
    req_data: ClassVar[dict] = configs[name]

    def _make_request(self, session: Session) -> Response:
        response = session.get(
            self.req_data.get('base_url'), headers=self.req_data.get('headers', {})
        )
        response.raise_for_status()
        return response

    def _parse(self, raw_data: dict) -> JobAddBase:
        return JobAddBase(
            source_id=raw_data.get('job_id'),
            title=raw_data.get('title'),
            slug=raw_data.get('slug'),
            url=raw_data.get('_links').get('detail_en').get('href'),
            company=raw_data.get('company_name'),
            source_website=self.name,
            employment_type=raw_data.get('employment_type_ids', list())[0],
            employment_rate=raw_data.get('employment_grades', list())[0],
            #category='',
            extent=str(raw_data.get('employment_grades', list())[0]),
            description=raw_data.get('preview'),
            location=raw_data.get('place'),
            publication_date=raw_data.get('publication_date'),
        )

    def scrape(self, session: Session) -> Iterable[JobAddBase]:
        res = self._make_request(session)
        for job_add in res.json()['documents']:
            yield self._parse(job_add)


def get_scraper(website_name: WebsiteNames) -> Scraper | None:
    return {
        WebsiteNames.academicwork: AcademicworkScraper,
        WebsiteNames.jobup: JobupScraper,
    }.get(website_name)()
