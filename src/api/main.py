from fastapi import FastAPI

from api.database import Base, engine
from api.routers.job_add_router import router as job_add_router

# Init modules
from api import scraping
scraping.init_module()

# Init app
app = FastAPI()
app.include_router(job_add_router)
