import asyncio
from typing import ClassVar, Iterable

from requests import Session, Response
import httpx

from api.schemas.job_add import JobAddBase
from api.schemas.website_names import WebsiteNames
from .base_scraper import BaseScraper


class JobupScraper(BaseScraper):
    """Class for parsing jobs data from jobup website."""

    name: ClassVar[str] = WebsiteNames.jobup

    async def _make_request(
        self,
        session: httpx.AsyncClient,
        alt_url: str | None = None,
        alt_body: dict | None = None,
    ) -> httpx.Response:
        response = await session.get(
            url=alt_url or self.req_data.q_base_url,
            headers=self.req_data.headers,
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
            # employment_type=raw_data.get('employment_type_ids', list())[0],
            # employment_rate=raw_data.get('employment_grades', list())[0],
            # category='',
            # extent=str(raw_data.get('employment_grades', list())[0]),
            description=raw_data.get('preview'),
            location=raw_data.get('place'),
            publication_date=raw_data.get('publication_date'),
        )

    async def scrape(
        self, session: Session, res_data: list[JobAddBase], max_page: int = 1
    ) -> Iterable[JobAddBase]:
        tasks = []

        # Initial request to get max number of available pages
        ini_response = await self._make_request(session)
        ini_data = ini_response.json()

        # Build async tasks
        for page_n in range(min(max_page, ini_data['num_pages'])):
            url = f'{self.req_data.q_base_url}&page={page_n+1}'
            tasks.append(self._make_request(session, alt_url=url))

        # Gather tasks result and parse
        responses = await asyncio.gather(*tasks)
        for resp in responses:
            data = resp.json()
            res_data.extend([self._parse(job_add) for job_add in data['documents']])
