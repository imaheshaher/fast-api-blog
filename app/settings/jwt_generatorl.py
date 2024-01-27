

from jose import JWTError, jwt
from datetime import datetime, timedelta,timezone

from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from typing import Union
from typing_extensions import Annotated
from app.models.user import TokenData
from app.controllers import get_user
# Secret key to sign the JWT token
SECRET_KEY = "BeSecure"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify the JWT token
def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token expire",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception



# Dependency to get the current user from the token
async def get_current_user(token: dict = Depends(verify_token)):
    return token