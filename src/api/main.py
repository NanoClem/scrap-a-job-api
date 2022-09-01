from fastapi import FastAPI

from api.routers.job_add_router import router as job_add_router
from api import scraping

# Init modules
scraping.init_module()

# Init app
app = FastAPI()
app.include_router(job_add_router)