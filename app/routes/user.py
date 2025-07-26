from app.models.users import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.utils.database import get_db
from fastapi import APIRouter, status, Depends, HTTPException
from app.utils.auth import hash_password, verify_password, create_access_token, get_current_user
from sqlalchemy.orm import Session

router = APIRouter(prefix='/users', tags=["user"])

@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email or User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=404, detail="Email or username already in use")
    hashed_password = hash_password(user.password)
    db_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully"}

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=404, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return{"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user