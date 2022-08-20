from fastapi import FastAPI

from api.database import Base, engine
from api.v1.router import router as v1_router

# Init database
Base.metadata.create_all(bind=engine)

# Init app
app = FastAPI()
app.include_router(v1_router)
