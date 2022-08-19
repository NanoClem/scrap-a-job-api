from enum import Enum
from typing import Optional, TypeVar, Generic

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T')


class WebsiteNames(str, Enum):
    academicwork = 'academicwork'
    jobup = 'jobup'


class ApiResponse(GenericModel, Generic[T]):
    code: int
    status: str
    message: str
    result: Optional[T] = None
    

class JobAddBase(BaseModel):
    source_id: Optional[str] = None
    title: Optional[str] = None
    slug: Optional[str] = None
    url: Optional[str] = None
    source_website: Optional[str] = None
    employment_type: Optional[str] = None
    job_category: Optional[str] = None
    job_extent: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    publication_date: Optional[str] = None
    employment_rate: Optional[int] = None
    company: Optional[str] = None 


class JobAdd(JobAddBase):
    id: int

    class Config:
        orm_modde = True
