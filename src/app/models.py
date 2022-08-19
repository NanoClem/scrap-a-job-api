from sqlalchemy import Column, Integer, String

from app.database import Base


class JobModel(Base):
    __tablename__ = 'job_adds'

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String, unique=True, index=True, nullable=False)
    title: Column(String)
    slug: Column(String)
    url: Column(String)
    source_website: Column(String)
    employment_type: Column(String)
    job_category: Column(String)
    job_extent: Column(String)
    description: Column(String)
    location: Column(String)
    publication_date: Column(String)
    employment_rate: Column(Integer)
    company: Column(String)
    