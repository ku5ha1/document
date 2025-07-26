from pydantic import BaseModel
from typing import List, Optional

class RecipeCreate(BaseModel):
    title: str 
    content: str 
    ingredients: List[str]
    steps: str 
    image_url: str 

class RecipeOut(BaseModel):
    id: int 
    title: str 
    content: str 
    ingredients: List[str]
    steps: str 
    image_url: str 
    user_id: int

    class Config:
        from_attributes = True 
    
class RecipeOwner(RecipeOut):
    owner: Optional[dict] = None