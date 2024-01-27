from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers import post as post_controller
from app.models.post import PostCreate, Post
from app.database.setting import get_db
from app.settings.jwt_generatorl import get_current_user

router = APIRouter()
router = APIRouter(dependencies=[current_user:=Depends(get_current_user)])

# API to create a new post
@router.post("/posts/", response_model=Post)
def create_post(post: PostCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return post_controller.create_post(db=db, post=post, user_id=current_user["id"])

# API to get all posts
@router.get("/posts/", response_model=list[Post])
async def read_all_posts(db: Session = Depends(get_db),current_user= current_user):
    user_id  = current_user["id"]
    return post_controller.get_all_posts(db=db,user_id=user_id)

# API to get a specific post by ID
@router.get("/posts/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    return post_controller.get_post(db=db, post_id=post_id)

# API to update a post by ID
@router.put("/posts/{post_id}", response_model=Post)
def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db),current_user= current_user):
    user_id  = current_user["id"]
    return post_controller.update_post(db=db, post_id=post_id, post=post,user_id=user_id)

# API to delete a post by ID
@router.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db),current_user= current_user):
    user_id  = current_user["id"]
    post_controller.delete_post(db=db, post_id=post_id,user_id=user_id)
    return {"message": "Post deleted successfully"}
