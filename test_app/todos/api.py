
from fastapi import APIRouter, Depends
from test_app.core.db import get_async_session
from test_app.todos import crud as todos_crud
from test_app.todos.schemas import todosSchema
router=APIRouter()
@router.get("/",response_model=list[todosSchema],status_code=200,)

async def get_todos(db=Depends(get_async_session)):
    todos=await todos_crud.get_todos(db)
    return todos

@router.post("/",response_model=todosSchema,status_code=201,)

async def create_todos(todos:todosSchema,db=Depends(get_async_session)):
    todos=await todos_crud.create_todos(db)
    return todos
    

