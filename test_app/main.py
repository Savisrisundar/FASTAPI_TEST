from fastapi import FastAPI,Request,status,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from test_app import settings
from test_app.core.db import get_async_session
from test_app.core.models import HealthCheck
from test_app.router.endpoints import api_router
from fastapi.staticfiles import StaticFiles
from test_app.users import crud as users_crud
from test_app.todos import crud as todos_crud
templates=Jinja2Templates(directory="c:/Users/Sundark/Desktop/FASTAPI_TEST/test_app/templates")
fastapi_app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    debug=settings.debug,
    templates="templates",
    
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token/")

@fastapi_app.get("/")
async def home(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})

@fastapi_app.get("/login", response_class=templates.TemplateResponse)
async def login_form(request: Request):
  context = {"request": request}
  return templates.TemplateResponse("login.html",context=context)

@fastapi_app.get("/user", response_class=templates.TemplateResponse)

async def get_user(request:Request):
    context={"request":request}
    return templates.TemplateResponse("users.html",context=context)

@fastapi_app.get("/usercreate", response_class=templates.TemplateResponse)

async def get_user(request:Request):
    context={"request":request}
    return templates.TemplateResponse("create_user.html",context=context)

@fastapi_app.get("/userupdate", response_class=templates.TemplateResponse)

async def get_user(request:Request,id:int,db=Depends(get_async_session)):
    user_by_id=await users_crud.get_user_by_id(id,db)
    if user_by_id.admin is True:
        raise HTTPException(status_code=404, detail="You can not change another Admin's details")
    print(user_by_id)
    context={"request":request,"user":user_by_id}
    return templates.TemplateResponse("update_user.html",context=context)


@fastapi_app.get("/userdelete", response_class=templates.TemplateResponse)

async def get_user(request:Request,id:int,db=Depends(get_async_session)):
    user_by_id=await users_crud.get_user_by_id(id,db)
    print(user_by_id)
    context={"request":request,"user":user_by_id}
    return templates.TemplateResponse("delete.html",context=context)

@fastapi_app.get("/userupdateme", response_class=templates.TemplateResponse)

async def get_user(request:Request,db=Depends(get_async_session)):
    username=await users_crud.get_saved_username()
    username1=await users_crud.get_user_by_username(db,username)
    user_by_id=await users_crud.get_user_by_id(username1.id,db)
    print(user_by_id.id)
    context={"request":request,"user":user_by_id}
    return templates.TemplateResponse("update_user_me.html",context=context)

@fastapi_app.get("/update_my_todo", response_class=templates.TemplateResponse)

async def get_user(request:Request,db=Depends(get_async_session)):
    username=await users_crud.get_saved_username()
    username1=await users_crud.get_user_by_username(db,username)
    todos=await todos_crud.get_todosid_by_ownerid(username1.id,db)
    todos=await todos_crud.get_todos_by_id(todos,db)
    context={"request":request,"user":todos}
    return templates.TemplateResponse("update_todos_me.html",context=context)

@fastapi_app.get("/todocreate", response_class=templates.TemplateResponse)

async def get_user(request:Request,db=Depends(get_async_session)):
    db_user1=await users_crud.get_saved_username()
    db_user=await users_crud.get_user_by_username(db,db_user1)
    user=[db_user.id]
    context={"request":request,"users":user}
    return templates.TemplateResponse("create_todo.html",context=context)

@fastapi_app.get("/tododelete", response_class=templates.TemplateResponse)

async def get_user(request:Request,db=Depends(get_async_session)):
    username=await users_crud.get_saved_username()
    username1=await users_crud.get_user_by_username(db,username)
    todos=await todos_crud.get_todosid_by_ownerid(username1.id,db)
    todos=await todos_crud.get_todos_by_id(todos,db)
    context={"request":request,"user":todos}
    return templates.TemplateResponse("delete_todo.html",context=context)






fastapi_app.include_router(api_router, prefix=settings.api_v1_prefix)
@fastapi_app.on_event("startup")
async def app_startup():
    print("app started")
    
@fastapi_app.on_event("shutdown")
async def pickle_schedule():
    print("app shut down")
    
@fastapi_app.get("/",response_model=HealthCheck, tags=["status"])
async def health_check():
    return{
        "name":settings.project_name,
        "version":settings.version,
        "description":settings.description
    }    
    

