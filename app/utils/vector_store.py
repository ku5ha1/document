from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from app.utils.pdf_loader import extract_and_save_text
from dotenv import load_dotenv 
import os 

load_dotenv()

def split_text_into_chunks(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len, 
        is_separator_regex=False
    )
    return splitter.split_text(text)

def create_vector_store(chunks: list[str]):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    return vector_store

# def test_function():
#     with open('data/processed/c791192d-a142-4a73-a4de-90b557611fbf.txt', "r", encoding="utf-8") as F:
#         text = F.read()
        # chunks = split_text_into_chunks(text)
        # store = create_vector_store(chunks=chunks)
#         res = store.similarity_search('Role of a QA Vendor in the scope?', k=2)
#         print(res)
        
# test_function()