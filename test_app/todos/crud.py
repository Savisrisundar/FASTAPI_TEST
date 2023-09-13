from sqlalchemy import select,update
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from test_app.todos.models import Todos
from test_app.todos.schemas import todosSchemaCreate,todosSchema,todosSchemaBase
async def get_todos(db:AsyncSession):
    statement=select(Todos)
    result=await db.execute(statement)
    todos=result.scalars().all()
    return todos
async def get_todosid_by_ownerid(id:int,db:AsyncSession):
    test=select(Todos).where(Todos.owner_id==id)
    result=await db.execute(test)
    todo=result.scalars().one_or_none
    net=todo
    if(net is None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no todos for this user",)
        

async def create_todos(db:AsyncSession,todo:todosSchemaCreate):
    db_todo=Todos(**todo.dict())
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

async def get_todos_by_id(db:AsyncSession,id:int):
    
    test=select(Todos)
    result=await db.execute(test)
    todo=result.scalars().all()
    for i in todo:
        if(i.id==id):
            return i
        
    


async def update_todos(id:int,todo:todosSchema,db:AsyncSession):
    todo_in_db = await db.get(Todos, id)
    if not todo_in_db:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_in_db.task_name = todo.task_name
    todo_in_db.status = todo.status
    todo_in_db.description=todo.description
    todo_in_db.duration=todo.duration

    await db.commit()

    return todo_in_db


async def delete_todos(id:int,db:AsyncSession):
    
    todo = await db.get(Todos, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    await db.delete(todo)
    await db.commit()

    return todo
    
    
    
    