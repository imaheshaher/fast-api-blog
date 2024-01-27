from pydantic import BaseModel,Field,EmailStr
from sqlalchemy import Column, Integer, String
from app.databases import Base
from typing import Optional,Union

class User(BaseModel):
    email: EmailStr
    password: str
    class Config:
        orm_mode = True

class LoginData(BaseModel):
    email: EmailStr
    password: str



class TokenData(BaseModel):
    username: Union[str, None] = None

# SQLAlchemy model
class DBUser(Base):
    __tablename__ = "user" 

    id = Column(String(255), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))

