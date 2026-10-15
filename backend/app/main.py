from fastapi import FastAPI
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.security import hash_password


app = FastAPI(title="SkillTrack LMS")


@app.get("/")
def home():
    return {"message": "Welcome to SkillTrack LMS!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )
    hashed_password = hash_password(user_data.password)
    new_user = User(name=user_data.name,email=user_data.email,password_hash=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
    "message": "User registered successfully",
    "user_id": new_user.id,
    "name": new_user.name,
    "email": new_user.email
}