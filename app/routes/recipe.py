from app.utils.database import get_db
from app.utils.auth import get_current_user
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.recipe import RecipeCreate, RecipeOut
from app.models.users import User
from app.models.recipe import Recipe
from typing import List

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.post("/create", response_model=RecipeOut)
async def create_recipe(recipe: RecipeCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_recipe = Recipe(
        title=recipe.title,
        content=recipe.content,
        ingredients=recipe.ingredients,
        steps=recipe.steps,
        image_url=recipe.image_url,
        user_id=current_user.id
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe 

@router.get("/all", response_model=List[RecipeOut])
async def get_all_recipes(db: Session = Depends(get_db)):
    recipes = db.query(Recipe).all()
    return recipes

@router.get("/{recipe_id}", response_model=RecipeOut)
async def get_single_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe

@router.put("/{recipe_id}", response_model=RecipeOut)
async def update_recipe(
    recipe_id: int,
    recipe_data: RecipeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )
    if recipe.user_id != current_user.id: # pyright: ignore[reportGeneralTypeIssues]
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this recipe"
        )
    setattr(recipe, "title", recipe_data.title)
    setattr(recipe, "content", recipe_data.content)
    setattr(recipe, "ingredients", recipe_data.ingredients)
    setattr(recipe, "steps", recipe_data.steps)
    setattr(recipe, "image_url", recipe_data.image_url)
    
    db.commit()
    db.refresh(recipe)
    return recipe

@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if recipe.user_id != current_user.id: # pyright: ignore[reportGeneralTypeIssues]
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this recipe"
        )   
    db.delete(recipe)
    db.commit()
    return {"message": "recipe deleted successfully"}