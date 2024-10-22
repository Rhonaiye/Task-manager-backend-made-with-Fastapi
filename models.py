from database import Base
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    
    todos = relationship('Todo', cascade='all,delete-orphan', back_populates='user')
    


class Todo(Base):
    __tablename__ = 'todos'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description =Column(String)
    complete = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship('Users', back_populates= 'todos')