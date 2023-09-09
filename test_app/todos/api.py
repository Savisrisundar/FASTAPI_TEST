
from fastapi import APIRouter, Depends, Request
from test_app.core.db import get_async_session
from test_app.todos import crud as todos_crud
from test_app.todos.schemas import todosSchema,todosSchemaCreate
router=APIRouter()
@router.get("/",response_model=list[todosSchema],status_code=200,)

async def get_todos(db=Depends(get_async_session)):
    todos=await todos_crud.get_todos(db)
    return todos

@router.post("/",response_model=todosSchema,status_code=201,)

async def create_todos(todos:todosSchemaCreate,db=Depends(get_async_session)):
    todos=await todos_crud.create_todos(db,todos)
    return todos

@router.put("/{id}",response_model=todosSchema,status_code=202)
async def update_todos(id:int,todos:todosSchema,db=Depends(get_async_session)):
    todos=await todos_crud.update_todos(id,todos,db)
    return todos
    
@router.delete("/{id}",status_code=200)

async def delete_todos(id:int,db=Depends(get_async_session)):
    todo=await todos_crud.delete_todos(id,db)
    return todo
