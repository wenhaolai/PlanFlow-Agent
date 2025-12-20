from enum import Enum
from typing import Optional, Union

from fastapi import FastAPI, Path, Query, Body, Cookie, Header, HTTPException, status, Depends
from fastapi.responses import JSONResponse

import os

from sqlalchemy.orm import Session
from sqlalchemy import text

from api.user import router as user_router
from api.chat import router as chat_router
from api.tasks import router as task_router
from core.mysql import get_db

# fastapi.Path/Query/Body支持url内参数的验证
# 其中Body可以将查询参数移到请求报文内，并且实现验证

# 在api的定义函数中使用 *, 进行修饰，使函数体内所有的参数都变为固定参数
# 调用函数时需要指定值对应的参数，而不是按顺序填入
# 这样就可以指定某个参数有示例值，而其它参数没有

# 使用status返回已经定义好的一些状态码
# HTTPException抛出异常，detail里填写返回的信息

# 或者使用自定义的异常处理函数，使用@app.exception_handler进行自定义异常处理

app = FastAPI()

app.include_router(user_router, prefix='/api')
app.include_router(chat_router, prefix='/api')
app.include_router(task_router, prefix='/api')

@app.get("/")
async def root():
    return {"message":  os.getenv("DASHSCOPE_API_KEY")}

@app.get("/health")
async def health(db_session: Session = Depends(get_db)):
    try:
        # 执行原生 SQL 查询所有用户
        result = db_session.execute(text("SELECT * FROM users"))
        rows = result.fetchall()
        
        # 将结果转换为字典列表
        users = []
        if rows:
            keys = result.keys()
            for row in rows:
                users.append(dict(zip(keys, row)))
        
        return {
            "status": "ok",
            "message": "Database connection successful",
            "total_users": len(users),
            "users": users
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}"
        )

# responses={400:{'model':ERROR_MESSAGE}, 401:...}