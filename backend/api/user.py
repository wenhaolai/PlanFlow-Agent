import os
from datetime import timedelta, datetime, timezone

import jwt
import uvicorn
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel

router = APIRouter()

SECURITY_KEY = os.environ.get("SECURITY_KEY", "qq_ncy9tw3YeRhoAKWHiiaqmgc4fF3uxOLr-X9eugZE")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login")

class Token(BaseModel):
    access_token: str
    token_type: str

def validate_user(username: str, password: str):
    if username == username and password == password:
        return username

    return None

def get_current_user(token: str = Depends(oauth2_schema)):
    try:
        token_data = jwt.decode(token, SECURITY_KEY, algorithms=[ALGORITHM])
        if token_data:
            username = token_data.get("username", None)
            return username
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post('/login', response_model=Token)
async def login(login_form: OAuth2PasswordRequestForm = Depends()):
    username = validate_user(login_form.username, login_form.password)
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})

    token_expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    token_data = {
        "username": username,
        "exp": token_expires
    }

    token = jwt.encode(token_data, SECURITY_KEY, algorithm=ALGORITHM)
    return Token(access_token=token, token_type="Bearer")

@router.get('/items')
async def get_items(username: str = Depends(get_current_user)):
    return {"current_user": username}

if __name__ == '__main__':
    uvicorn.run(reload=True)