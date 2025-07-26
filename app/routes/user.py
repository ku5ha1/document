from app.models.users import User
from app.schemas.user import UserCreate
from app.utils.database import get_db
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix='users', tags=["user"])

