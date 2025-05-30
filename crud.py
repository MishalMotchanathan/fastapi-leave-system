import email
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from auth import hash_password

def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = User(username = user.userName, email = user.email, hashed_password = hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    