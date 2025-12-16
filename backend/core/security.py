"""
处理密码加密和Token生成
"""
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional, Dict
import jwt
import bcrypt
from fastapi import HTTPException, status
from .config import settings

logger = logging.getLogger(__name__)

def create_access_token(subject: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    生成JWT Access Token
    :param subject: 主题（通常是用户ID）
    :param expires_delta: 过期时间增量
    :return: 加密后的Token字符串
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    
    # 将用户id(sub)和生成时间(iat)包装进token
    to_encode = {
        "exp": expire, 
        "sub": str(subject), 
        "iat": datetime.now(timezone.utc)
    }
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """
    解析JWT Token
    :param token: Token字符串
    :return: 解析后的Payload字典，如果无效或过期则返回None
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")
    except jwt.InvalidTokenError:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的Token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    """
    try:
        # bcrypt需要bytes类型
        if isinstance(plain_password, str):
            plain_password = plain_password.encode('utf-8')
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
            
        return bcrypt.checkpw(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"密码验证失败：{e}", exc_info=True)
        return False

def get_password_hash(password: str) -> str:
    """
    获取密码哈希值
    """
    if isinstance(password, str):
        password = password.encode('utf-8')
    # 生成salt并hash
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed.decode('utf-8')



