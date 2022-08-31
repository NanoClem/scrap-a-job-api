from typing import Optional

from pydantic import BaseModel


class JobAddBase(BaseModel):
    source_id: Optional[str] = None
    title: Optional[str] = None
    slug: Optional[str] = None
    url: Optional[str] = None
    company: Optional[str] = None
    source_website: Optional[str] = None
    employment_type: Optional[str] = None
    employment_rate: Optional[int] = None
    category: Optional[str] = None
    extent: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    publication_date: Optional[str] = None


class JobAdd(JobAddBase):
    id: int

    class Config:
        orm_mode = True
