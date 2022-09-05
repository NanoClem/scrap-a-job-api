import asyncio
from typing import ClassVar

import httpx

from api.schemas.job_add import JobAddBase
from api.schemas.website_names import WebsiteNames
from .base_scraper import BaseScraper
from ..utils import parse_cookies


class AcademicworkScraper(BaseScraper):
    """Class for parsing jobs data from academicwork website."""

    name: ClassVar[str] = WebsiteNames.academicwork

    async def _make_request(
        self,
        session: httpx.AsyncClient,
        alt_url: str | None = None,
        alt_body: dict | None = None,
    ) -> httpx.Response:
        response = await session.post(
            url=self.req_data.base_url,
            headers=self.req_data.headers,
            json=alt_body or self.req_data.body,
            cookies=parse_cookies(self.req_data.raw_cookie),
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

    async def scrape(
        self, session: httpx.AsyncClient, res_data: list[JobAddBase], max_page: int = 1
    ) -> None:
        tasks = []
        curr_body = self.body

        # Initial request to get max number of available pages
        ini_response = await self._make_request(session, alt_body=curr_body)
        ini_resp_data = ini_response.json()

        # Build async tasks
        for _ in range(min(max_page, ini_resp_data['TotalIndexes'])):
            curr_body['StartIndex'] += 1
            tasks.append(self._make_request(session, curr_body))

        # Gather tasks result and parse
        responses = await asyncio.gather(*tasks)
        for resp in responses:
            data = resp.json()
            res_data.extend([self._parse(job_add) for job_add in data['Adverts']])
