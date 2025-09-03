from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
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
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    return vector_store