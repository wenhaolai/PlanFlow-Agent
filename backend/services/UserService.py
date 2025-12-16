from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from core.mysql import get_db
from core.security import decode_access_token
from models.UserModel import User
import ast

# 使用 HTTPBearer 替代 OAuth2PasswordBearer，以便在 Swagger UI 中手动输入 Token
# 这样兼容 JSON 登录接口（OAuth2PasswordBearer 默认要求 Form 表单登录）
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    """
    获取当前登录用户
    作为FastAPI依赖使用，验证Token并返回用户对象
    """
    token = credentials.credentials
    print(f"token={token}")
    # 解析Token
    payload = decode_access_token(token)
    print(f"payload={payload}")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 获取用户ID
    sub = payload.get("sub")
    user_id = None
    try:
        # 尝试解析字典字符串 "{'user_id': 2}"
        if isinstance(sub, str) and sub.strip().startswith("{"):
            sub_dict = ast.literal_eval(sub)
            if isinstance(sub_dict, dict):
                user_id = sub_dict.get("user_id")
        else:
            user_id = sub
    except Exception:
        pass

    print(f"user_id={user_id}")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 查询数据库获取用户信息
    user = db.query(User).filter(User.id == user_id).first()
    print(f"user={user}")
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return user

def verify_token_status(token: str) -> bool:
    """
    验证Token状态（仅返回布尔值）
    """
    payload = decode_access_token(token)
    return payload is not None