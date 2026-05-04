from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.dependencies import get_db, get_current_user
from app.models.models import User
from app.schemas.schemas import UserRead, UserUpdate

router = APIRouter(prefix="/users")


@router.get("", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).filter(User.is_active == True).all()


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/me", response_model=UserRead)
def update_me(update: UserUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if update.name is not None:
        user.name = update.name
    if update.email is not None:
        existing = db.query(User).filter(User.email == update.email, User.id != user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already taken")
        user.email = update.email
    db.commit()
    db.refresh(user)
    return user
