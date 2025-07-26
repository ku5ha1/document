from app.utils.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

class User(Base):
    __table__name = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Integer, index=True, unique=True, nullable=False)  
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
