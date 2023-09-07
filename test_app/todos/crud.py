from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from test_app.todos.models import Todos
async def get_todos(db:AsyncSession):
    statement=select(Todos)
    result=await db.execute(statement)
    todos=result.scalars().all()
    return todos
