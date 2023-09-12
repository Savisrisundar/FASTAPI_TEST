from test_app.core.db import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    fullname=Column(String,index=True)
    username=Column(String,unique=True, index=True)
    email=Column(String,unique=True,index=True)
    hashed_password=Column(String,nullable=False)
    is_active=Column(Boolean(), default=True)
    admin=Column(Boolean(),default=False)
    todos=relationship("Todos",back_populates="owner")
    
    
    