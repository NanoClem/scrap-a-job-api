from fastapi import FastAPI
from dotenv import load_dotenv

from app.database import Base, engine
from app.v1.router import router as v1_router

# Load env variables
load_dotenv()

# Init database
Base.metadata.create_all(engine)

# Init app
app = FastAPI()
app.include_router(v1_router)
