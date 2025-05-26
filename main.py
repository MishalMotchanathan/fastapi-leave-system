from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from auth import router as auth_router
from models import User
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

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
