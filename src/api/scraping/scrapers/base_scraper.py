from abc import ABC, abstractmethod
from typing import Iterable

import httpx

from ...schemas.job_add import JobAddBase
from ...schemas.website_names import WebsiteNames
from ..configs import RequestConfig, get_request_config


class BaseScraper(ABC):
    """Abstract class for jobs data parsing."""

    @property
    @abstractmethod
    def name(self) -> WebsiteNames:
        """Name of the parser"""

    @property
    def req_data(self) -> RequestConfig:
        """Data used to make requests."""
        return get_request_config(self.name)

    @property
    def body(self) -> dict:
        """Copy of request body in configs."""
        return self.req_data.body.copy()

    @abstractmethod
    async def _make_request(
        self,
        session: httpx.AsyncClient,
        alt_url: str | None = None,
        alt_body: dict | None = None,
    ) -> httpx.Response:
        """Make a http request using defined configuration."""

    @abstractmethod
    def _parse(self, raw_data: dict) -> JobAddBase:
        """Parse raw data into data schemas class."""

    @abstractmethod
    async def scrape(
        self, session: httpx.AsyncClient, res_data: list[JobAddBase], max_page: int = 1
    ) -> Iterable[JobAddBase]:
        """Scrape and parse data obtained from a request."""
