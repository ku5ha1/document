from fastapi import FastAPI  
from app.utils.database import Base, get_db, engine

app = FastAPI()

def init_db():
    Base.metadata.create_all(bind=engine)

@app.get("/")
async def get_root():
    return {"message": "App running"}

@app.on_event("startup")
async def startup_event():
    init_db()