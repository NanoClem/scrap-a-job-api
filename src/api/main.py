from fastapi import FastAPI

from api.database import Base, engine
from api.v1.router import router as v1_router
from api import scraping

# Init database
Base.metadata.create_all(bind=engine)

# Init scraping module
scraping.init_module()

# Init app
app = FastAPI()
app.include_router(v1_router)
