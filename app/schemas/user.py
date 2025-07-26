from pydantic import BaseModel
from app.models.users import User 
from datetime import datetime

class UserCreate(BaseModel):
    username: str 
    email: str 
    password: str

class UserResponse(BaseModel):
    username: str 
    email: str 
    created_at: datetime

class UserLogin(BaseModel):
    username: str 
    password: str

class UserOut(BaseModel):
    id: int 
    created_at: datetime

    class Config:
        orm_mode = True