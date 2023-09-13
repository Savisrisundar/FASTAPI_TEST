
from fastapi import APIRouter, Depends, Request,HTTPException,status
from test_app.core.db import get_async_session
from test_app.todos import crud as todos_crud
from test_app.users import crud as users_crud
from test_app.todos.schemas import todosSchema,todosSchemaCreate
router=APIRouter()
@router.get("/{owner_id}",response_model=todosSchema|None,status_code=200,)

async def get_todos(id:int,db=Depends(get_async_session)):
    print(id)
    todos1=await todos_crud.get_todosid_by_ownerid(id,db)
    todos=await todos_crud.get_todos_by_id(todos1,db)
    return todos
    
@router.post("/{username}",response_model=todosSchema,status_code=201,)

async def create_todos(username:str,password:str,todos:todosSchemaCreate,db=Depends(get_async_session)):
    db_user=await users_crud.get_password(db,username)
    
    db_user1=await users_crud.verify_password(password,db_user)
    if(db_user1 is True):
        todos=await todos_crud.create_todos(db,todos)
        return todos
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="unauthorized",)
    
    

@router.put("/{owner_id}",response_model=todosSchema,status_code=202)
async def update_todos(id:int,todos:todosSchema,db=Depends(get_async_session)):
    todos1=await todos_crud.get_todosid_by_ownerid(id,db)
    todos=await todos_crud.update_todos(todos1,todos,db)
    return todos
    
@router.delete("/{owner_id}",status_code=200)

async def delete_todos(id:int,db=Depends(get_async_session)):
    todos1=await todos_crud.get_todosid_by_ownerid(id,db)
    todo=await todos_crud.delete_todos(todos1,db)
    return todo
