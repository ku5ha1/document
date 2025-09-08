from fastapi import FastAPI, Request, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
import os, uuid
from app.utils.pdf_loader import extract_and_save_text
from app.utils.vector_store import split_text_into_chunks, create_vector_store
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
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
        extracted_text = extract_and_save_text(file_path)

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
    
@app.post('/ask')
async def ask_question(question: str):
    question = question 
    processed_dir = "data/processed"
    txt_files = [os.path.join(processed_dir, f) for f in os.listdir(processed_dir) if f.endswith(".txt")]
    latest_file = max(txt_files, key=os.path.getctime)

    with open(latest_file, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = split_text_into_chunks(text)
    store = create_vector_store(chunks=chunks)
    res = store.similarity_search(question, k=2)
            
    context = "\n\n".join([doc.page_content for doc in res])
    
    prompt = f"""
    Based on the following context - answer this question thouroughly and accurately. 
    
    Context: {context} 
    Question: {question}
    Answer:     
    """
    
    try: 
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
        answer = llm.invoke(prompt)
        return {
            "question" : question,
            "answer": answer.content    
                }
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail="Could not generate response. Try again later."
        )