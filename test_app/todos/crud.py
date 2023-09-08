from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from test_app.todos.models import Todos
from test_app.todos.schemas import todosSchemaCreate
async def get_todos(db:AsyncSession):
    statement=select(Todos)
    result=await db.execute(statement)
    todos=result.scalars().all()
    return todos

async def create_todos(db:AsyncSession,todo:todosSchemaCreate):
    db_todo=Todos(**todo.dict())
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo
    