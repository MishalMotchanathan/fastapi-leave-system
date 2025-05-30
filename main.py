import http
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from auth import router as auth_router
import models, schemas
from utils import hash_password

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Dependency for DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    return {"message": "Database connected successfully!"}

# Include auth routes
app.include_router(auth_router)


@app.post("/register")
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(
        (models.User.userName == user.userName) |
        (models.User.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exist.")

    hashed_pw = hash_password(user.password)
    new_user = models.User(
        userName = user.userName,
        email = user.email,
        hashed_password = hashed_pw,
        role = "employee",
        is_active = True
    )
    db.add(new_user)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    db.refresh(new_user)

    return {
        "message":"User registered Successfully",
        "user": {
            "userId": new_user.userId,
            "userName": new_user.userName,
            "email": new_user.email
        }
    }