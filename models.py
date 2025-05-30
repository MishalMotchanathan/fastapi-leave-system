from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema":"hr"}

    userId = Column(Integer, primary_key = True, index = True)
    userName = Column(String(150), unique = True, index = True, nullable = False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="employee")
    is_active = Column(Boolean, default=True)