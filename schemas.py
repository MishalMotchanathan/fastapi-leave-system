from re import A
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    userName: str = Field(..., alias="userName")
    email: EmailStr
    password: str

    class Config:
        allow_population_by_field_name = True
        