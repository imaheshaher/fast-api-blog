from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import controllers
from app.models.user import User,LoginData 
from app.settings.jwt_generatorl import create_access_token,get_current_user
from app.database.setting import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated

router = APIRouter()


@router.post("/signup/", response_model=User)
def create_user(user: User, db: Session = Depends(get_db)):
    return controllers.create_user(db=db, email=user.email, password=user.password)

@router.get("/user/me", response_model=User)
def read_user(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    user_id = current_user['id']
    db_user = controllers.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/login/", response_model=dict)
async def login(login_data: LoginData,db: Session = Depends(get_db)):
    db_user = controllers.login_user(db, login_data)

    if db_user:
        # Create a JWT token with user information
        token_data = {"email": db_user.email, "id": db_user.id}
        jwt_token = create_access_token(token_data)

        # Return the JWT token in the response
        return {"message": "Login successful", "token": jwt_token, "data": db_user.email}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")



@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: Session = Depends(get_db)):
    db_user = controllers.login_user(db, LoginData(**{"email":form_data.username,"password": form_data.password}))

    if db_user:
        # Create a JWT token with user information
        token_data = {"email": db_user.email, "id": db_user.id}
        jwt_token = create_access_token(token_data)

        # Return the JWT token in the response
        return {"message": "Login successful", "access_token": jwt_token, "data": db_user.email}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

