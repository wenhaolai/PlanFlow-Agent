from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict

from core.constants import MIN_USERNAME_LENGTH, MAX_USERNAME_LENGTH, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH


class UserCreate(BaseModel):
    """注册用户的请求schema，目前包含简单的输入验证"""
    username: str = Field(..., min_length=MIN_USERNAME_LENGTH, max_length=MAX_USERNAME_LENGTH, description="用户名")
    password: str = Field(..., min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH, description="密码")
    email: EmailStr = Field(..., description="用户邮箱") # 邮箱为必要字段
    bio: Optional[str] = Field(None, description="用户简介(可选)")

class UserLogin(BaseModel):
    """请求登录schema"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH, description="登陆密码")

class UserResponse(BaseModel):
    """用户响应schema，不包含敏感信息"""
    id: int
    username: str
    email: EmailStr
    bio: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True) # 启用ORM模式，允许Pydanic直接从SQLAlchemy读取数据，不用中间手动转化为字典


class UserLoginResponse(BaseModel):
    """成功登录响应schema"""
    access_token: str = Field(...)
    token_type: str = "bearer"