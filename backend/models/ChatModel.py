from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from core.mysql import Base

class Chat(Base):
    __tablename__ = 'chat'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='聊天ID')
    task_id = Column(Integer, ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False, comment='所属任务ID')
    role = Column(String(50), nullable=False, comment='角色')
    content = Column(Text, nullable=False, comment='对话内容')
    timestamp = Column(TIMESTAMP, server_default=func.now(), comment='时间戳')

    # Relationships
    task = relationship("Task", back_populates="chats")
