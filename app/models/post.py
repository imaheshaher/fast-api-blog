# app/models/post.py
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, ForeignKey
from app.databases import Base
from typing import Optional

class PostCreate(BaseModel):
    title: str
    description: str

class Post(PostCreate):
    id: int
    user_id: str

    class Config:
        orm_mode = True

# SQLAlchemy model
class DBPost(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String(255))
    user_id = Column(String(255), ForeignKey("user.id"))
