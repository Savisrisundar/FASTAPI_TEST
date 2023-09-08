from test_app.core.db import Base
from sqlalchemy import Column,Integer, String, Boolean, DateTime
class Todos(Base):
    __tablename__="TODOS"
    
    id=Column(Integer,primary_key=True, index=True)
    task_name=Column(String,unique=True,index=True)
    description=Column(String,index=True)
    duration=Column(DateTime)
    status=Column(String,index=True)
    
    