from sqlalchemy.orm import Session
from app.models.user import DBUser,LoginData
from uuid import uuid4
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, HTTPException, Depends

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, email: str, password: str):
    # Check if user with the given email already exists
    existing_user = db.query(DBUser).filter(DBUser.email == email).first()
    if existing_user:
        raise ValueError("User with this email already exists")

    try:
        hashed_password = pwd_context.hash(password)
        db_user = DBUser(email=email, password=hashed_password, id=str(uuid4()))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(e, "error-->")
        raise ValueError("Error creating user")

def get_user(db: Session, user_id: int):
    return db.query(DBUser).filter(DBUser.id == user_id).first()  
def get_all_user(db:Session):
    return db.query(DBUser).all()
def get_user_by_email(db: Session, email: str):
    return db.query(DBUser).filter(DBUser.email == email).first()  

def login_user(db: Session, login_data: LoginData = Depends()):
    db_user = db.query(DBUser).filter(DBUser.email == login_data.email).first()

    # Verify the password
    if db_user is None or not pwd_context.verify(login_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return db_user



    

