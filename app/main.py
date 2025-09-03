from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
from pathlib import Path

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
TEMPLATES = Jinja2Templates(directory="templates")

@app.get("/health")
async def get_health():
    return {"message": "App pinged successfully"}

@app.get("/")
async def homepage(request: Request):
    context = {"request": request}
    return TEMPLATES.TemplateResponse("home.html", context=context)