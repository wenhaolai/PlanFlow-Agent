import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from core.constants import ErrorMessages
from core.mysql import get_db
from core.security import get_password_hash, verify_password, create_access_token
from models.UserModel import User
from schemas.UserSchema import UserLogin, UserResponse, UserCreate, UserLoginResponse
from services.UserService import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/user/register", response_model=UserResponse)
async def register(
        user_data: UserCreate,
        db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessages.EMAIL_EXISTS)

    existing_user = db.query(User).filter(User.email == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorMessages.USERNAME_EXISTS)

    # 创建用户
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_password,
        bio = user_data.bio
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    logger.info(f"创建用户：{user_data.username}，ID is {db_user.id}")
    return db_user

@router.post("/user/login", response_model=UserLoginResponse)
async def login(
        user_login_data: UserLogin,
        db: Session = Depends(get_db)
):
    # 可以使用用户名或者密码进行登录
    user = db.query(User).filter(
        or_(
            User.username == user_login_data.username,
            User.email == user_login_data.username
        )
    ).first()

    if not user or not verify_password(user_login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user.last_login = datetime.now()
    db.commit()

    access_token = create_access_token(subject={"user_id": user.id})

    return UserLoginResponse(
        access_token=access_token,
        token_type="bearer"
    )

@router.get("/user/profile", response_model=UserResponse)
async def get_profile(
        current_user: User = Depends(get_current_user)
):
    return current_user    