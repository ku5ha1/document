from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
import os, uuid
 
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

ALLOWED_CONTENT_TYPE = 'application/pdf'
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "data")

@app.post("/upload")
async def upload_file(request: Request, file: UploadFile):
    if file.content_type != ALLOWED_CONTENT_TYPE:
        return TEMPLATES.TemplateResponse(
            "home.html",
            {
                "request": request,
                "error": f"Invalid file type. Only PDFs are allowed."
            },
            status_code=400
        )

    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    except OSError as e:
        return TEMPLATES.TemplateResponse(
            "home.html",
            {
                "request": request,
                "error": f"Failed to create upload directory: {str(e)}"
            },
            status_code=500
        )

    unique_filename = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())

        return TEMPLATES.TemplateResponse(
            "home.html",
            {
                "request": request,
                "success": f"File '{unique_filename}' uploaded successfully!"
            },
            status_code=200
        )
    except Exception as e:
        return TEMPLATES.TemplateResponse(
            "home.html",
            {
                "request": request,
                "error": f"Failed to save file: {str(e)}"
            },
            status_code=500
        )