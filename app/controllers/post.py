from sqlalchemy.orm import Session
from app.models.post import PostCreate, Post,DBPost
from app.models.user import DBUser
from typing import List

def create_post(db: Session, post: PostCreate, user_id: str):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()

    if db_user:
        db_post = DBPost(**post.dict(), user_id=user_id)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    else:
        raise ValueError("User not found")

def get_all_posts(db: Session,user_id:str) -> List[Post]:
    return db.query(DBPost).filter(DBPost.user_id ==user_id )

def get_post(db: Session, post_id: int) -> Post:
    return db.query(DBPost).filter(DBPost.id == post_id).first()

def update_post(db: Session, post_id: int, post: PostCreate, user_id: str) -> Post:
    db_post = db.query(DBPost).filter(DBPost.id == post_id,DBPost.user_id==user_id).first()

    if db_post:
        for key, value in post.dict().items():
            setattr(db_post, key, value)
        
        db.commit()
        db.refresh(db_post)
        return db_post
    else:
        raise ValueError("Post not found")

def delete_post(db: Session, post_id: int,user_id:str):
    db_post = db.query(DBPost).filter(DBPost.id == post_id, DBPost.user_id == user_id).first()

    if db_post:
        db.delete(db_post)
        db.commit()
    else:
        raise ValueError("Post not found")
