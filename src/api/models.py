from sqlalchemy import Column, Integer, String

from .database.database import Base


class JobModel(Base):
    __tablename__ = 'job_adds'

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String)
    slug = Column(String)
    url = Column(String)
    company = Column(String)
    source_website = Column(String)
    employment_type = Column(String)
    employment_rate = Column(Integer)
    category = Column(String)
    extent = Column(String)
    description = Column(String)
    location = Column(String)
    publication_date = Column(String)
