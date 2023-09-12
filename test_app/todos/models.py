from test_app.core.db import Base
from pydantic import BaseModel
from test_app.users.models import User
from sqlalchemy import Column,Integer, String, Boolean, DateTime,ForeignKey,Enum
from sqlalchemy.orm import relationship
class Todos(Base):
    __tablename__="TODOS"
    
    id=Column(Integer,primary_key=True, index=True)
    task_name=Column(String,unique=True,index=True)
    description=Column(String,index=True)
    duration=Column(Integer)
    status=Column(String,index=True)
    owner=relationship("User",back_populates="todos")
    owner_id=Column(Integer,ForeignKey("users.id"))
    
    