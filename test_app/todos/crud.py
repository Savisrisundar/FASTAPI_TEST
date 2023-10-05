from sqlalchemy import select
from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from test_app.todos.models import Todos
from test_app.todos.schemas import todosSchemaCreate,todosSchema

async def get_todos(db:AsyncSession):
    statement=select(Todos)
    result=await db.execute(statement)
    todos=result.scalars().all()
    return todos

async def get_todosid_by_ownerid(id:int,db:AsyncSession):
    statement=select(Todos).where(Todos.owner_id==id)
    result=await db.execute(statement)
    todo=result.scalars().one_or_none()
    
    if todo is None:
        todos=None
    else:
        todos=todo.id
    
    return todos
async def check_for_todo(id:int,db:AsyncSession):
    statement=select(Todos).where(Todos.owner_id==id)
    result=await db.execute(statement)
    todo=result.scalars().one_or_none()
    
    if todo is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="todos for this user already existing",)
    else :
        return True
        

async def create_todos(db:AsyncSession,todo:todosSchemaCreate):
    db_todo=Todos(**todo.dict())
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

async def get_todos_by_id(id:int,db:AsyncSession):
    todo = await db.get(Todos, id)
    return todo
    
async def update_todos(id:int,todo:todosSchema,db:AsyncSession):
    todo_in_db = await db.get(Todos, id)
    if not todo_in_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_in_db.task_name = todo.task_name
    todo_in_db.status = todo.status
    todo_in_db.description=todo.description
    todo_in_db.duration=todo.duration
    print(todo_in_db.description)
    await db.commit()
    return todo_in_db


async def delete_todos(id:int,db:AsyncSession):
    todo = await db.get(Todos, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    await db.delete(todo)
    await db.commit()
    return todo
    
    
    
    