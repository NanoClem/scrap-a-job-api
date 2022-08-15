from enum import Enum

from pydantic import BaseModel


class WebsiteNames(str, Enum):
    academicwork = 'academicwork'
    jobup = 'jobup'


class JobAddBase(BaseModel):
    source_id: str
    title: str
    slug: str
    url: str
    source_website: str
    employment_type: str
    job_category: str
    job_extent: str
    description: str
    location: str
    publication_date: str
    employment_rate: int = None
    company: str = None


class JobAddCreate(JobAddBase):
    pass


class JobAdd(JobAddBase):
    id: int

    class Config:
        orm_modde = True
