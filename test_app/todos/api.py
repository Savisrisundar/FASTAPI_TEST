
from fastapi import APIRouter, Depends,Request,Form
from test_app.core.db import get_async_session
from test_app.todos import crud as todos_crud
from test_app.users import crud as users_crud
from fastapi.templating import Jinja2Templates
from test_app.todos.schemas import todosSchema,todosSchemaCreate
templates=Jinja2Templates(directory="templates")
router=APIRouter()

@router.get("/id",response_class=templates.TemplateResponse,response_model=todosSchema|None,status_code=200,)

async def get_todos(request:Request,id:int,db=Depends(get_async_session)):
    print(id)
    db_user1=await users_crud.get_saved_username()
    db_user=await users_crud.get_user_by_username(db,db_user1)
    todos1=await todos_crud.get_todosid_by_ownerid(id,db)
    todos=await todos_crud.get_todos_by_id(todos1,db)
    error_msg=None
    if todos is None:
        error_msg="No todos for this user"
    if error_msg:
        if error_msg:
            context={"request":request,"error_msg": error_msg}
        if db_user.admin is True:
            return templates.TemplateResponse("users_todo.html",context=context)
        else:
            return templates.TemplateResponse("users_not_admin_todo.html",context=context)
    todo_schema = todosSchema.model_validate(todos,from_attributes=True)
    todo_schema=dict(todo_schema)
    todo_schema_list = list(todo_schema.values())
    print(todo_schema_list)
    return templates.TemplateResponse("display_todos.html",{"request":request,"users": todo_schema_list})
    
    
@router.post("/create_my_todo",response_class=templates.TemplateResponse,response_model=todosSchema,status_code=201)

async def create_todos(request:Request,task_name:str=Form(...),description:str=Form(...),duration:int=Form(...),status:str=Form(...),owner_id:int=Form(...),db=Depends(get_async_session)):
    check=await todos_crud.check_for_todo(owner_id,db)
    ex_todos_read={
    "task_name":task_name,
    "description":description,
    "duration":duration,
    "status":status,
    "id":4,
    "owner_id":owner_id,
     }
    
    async def update_user2(todo1:todosSchemaCreate,db=Depends(get_async_session)):
        todos=await todos_crud.create_todos(db,todo1)
        return todos
    output=await update_user2(todosSchemaCreate(**ex_todos_read),db) 
    output = todosSchema.model_validate(output,from_attributes=True)
    output=dict(output)
    print(output)
    user_schema_list = list(output.values())
    return templates.TemplateResponse("display_todos.html",{"request":request,"users": user_schema_list})
    

@router.post("/update_me",response_class=templates.TemplateResponse,response_model=todosSchema,status_code=202)

async def update_todos(request:Request,task_name:str=Form(...),description:str=Form(...),duration:int=Form(...),status:str=Form(...),id:int=Form(...),owner_id:int=Form(...),db=Depends(get_async_session)):
    print(task_name)
    ex_todos_read={
    "id":id,
    "task_name":task_name,
    "description":description,
    "duration":duration,
    "status":status,
    "owner_id":owner_id,
     }
    
    async def update_user2(todo1:todosSchema,db=Depends(get_async_session)):
        username=await users_crud.get_saved_username()
        username1=await users_crud.get_user_by_username(db,username)
        todos1=await todos_crud.get_todosid_by_ownerid(username1.id,db)
        todos=await todos_crud.update_todos(todos1,todo1,db) 
        return todos
    output=await update_user2(todosSchema(**ex_todos_read),db)
    user=await todos_crud.get_todosid_by_ownerid(output.owner_id,db)  
    output = todosSchema.model_validate(output,from_attributes=True)
    output=dict(output)
    user_schema_list = list(output.values())
    return templates.TemplateResponse("display_todos.html",{"request":request,"users": user_schema_list})
    
@router.post("/delete_my_todo",response_class=templates.TemplateResponse,status_code=200)

async def delete_todos(request:Request,owner_id:int=Form(...),db=Depends(get_async_session)):
    todos1=await todos_crud.get_todosid_by_ownerid(owner_id,db)
    todo=await todos_crud.delete_todos(todos1,db)
    user=[owner_id]
    context={"request":request,"user":user}
    return templates.TemplateResponse("display_delete.html",context=context)
    
