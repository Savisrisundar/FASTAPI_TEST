from pydantic import BaseModel
from test_app.todos.examples import ex_todos_create, ex_todos_read
from datetime import datetime



class todosSchemaBase(BaseModel):
    task_name:str
    description:str
    duration:int
    status:str
    owner_id:int

class todosSchemaCreate(todosSchemaBase):
    status:str
    class Config:
        schema_extra={"example":ex_todos_create}
        
class todosSchema(todosSchemaBase):
    id:int
    
    class Config:
        orm_mode=True
        schema_extra={"example":ex_todos_read}
