from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from core.mysql import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username = Column(String(50), unique=True, nullable=False, comment='用户名')
    password_hash = Column(String(255), nullable=False, comment='密码哈希')
    email = Column(String(100), unique=True, nullable=False, comment='电子邮件')
    bio = Column(Text, comment='用户简介')
    last_login = Column(TIMESTAMP, nullable=True, comment='最后登录时间')
    created_at = Column(TIMESTAMP, server_default=func.now(), comment='创建时间')
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    

