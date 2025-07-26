from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from app.utils.database import Base 
from sqlalchemy.orm import relationship

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    ingredients = Column(JSON)
    steps = Column(String)
    image_url = Column(String)
    owner_id = Column()

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship("User", back_populates="recipes")