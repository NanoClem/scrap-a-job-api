from api.schemas.website_names import WebsiteNames
from .base_scraper import BaseScraper
from .academicwork import AcademicworkScraper
from .jobup import JobupScraper


def get_scraper(website_name: WebsiteNames) -> BaseScraper | None:
    return {
        WebsiteNames.academicwork: AcademicworkScraper,
        WebsiteNames.jobup: JobupScraper,
    }.get(website_name)()