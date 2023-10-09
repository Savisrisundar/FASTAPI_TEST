from fastapi import APIRouter, Depends,Request,Form
from fastapi.templating import Jinja2Templates
from typing import List
from test_app.core.db import get_async_session
from test_app.users.schemas import UserSchema,UserSchemaCreate,Token
from test_app.users import crud as users_crud
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from fastapi.security import OAuth2PasswordBearer
templates=Jinja2Templates(directory="c:/Users/Sundark/Desktop/FASTAPI_TEST/test_app/templates")
router=APIRouter()

JWT_SECRET="savi"
ALGORITHM="HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token/")
payloads={}
def get_pays():
    return payloads



@router.get("/me",response_model=UserSchema, status_code=200)

async def get_me(request:Request,db=Depends(get_async_session)):
    username=await users_crud.get_saved_username()
    username1=await users_crud.get_user_by_username(db,username)
    user_schema = UserSchema.from_orm(username1)
    user_schema=dict(user_schema)
    user_schema_list = list(user_schema.values())
    print(user_schema)
    return templates.TemplateResponse("display_user.html",{"request":request,"users": user_schema_list})

@router.get("/all_user",response_model=List[UserSchema],status_code=200,dependencies=[Depends(users_crud.check_admin)])
async def get_all(request:Request,db=Depends(get_async_session)):
    username=await users_crud.get_users(db)
    return templates.TemplateResponse("display_all.html",{"request":request,"users":username})


@router.get("/username",response_model=UserSchema|None|dict, status_code=200,dependencies=[Depends(users_crud.check_admin)])

async def get_user(request:Request,username:str,db=Depends(get_async_session)):
    user=await users_crud.get_user_by_username(db,username)  
    error_msg=None
    if user is None:
        error_msg="This username not found"  
    if error_msg:
        context={"request":request,"error_msg": error_msg}
        return templates.TemplateResponse("users.html", context=context)
    user_schema = UserSchema.from_orm(user)
    user_schema=dict(user_schema)
    user_schema_list = list(user_schema.values())
    return templates.TemplateResponse("display_user.html",{"request":request,"users": user_schema_list})


@router.post("/create",response_class=templates.TemplateResponse,response_model=UserSchema, status_code=201,dependencies=[Depends(users_crud.check_admin)])

async def create_user(request:Request,fullname:str=Form(...),email:str=Form(...),username:str=Form(...),password:str=Form(...),is_active:str=Form(...),admin:str=Form(...),db=Depends(get_async_session)):
    
    ex_user_create={
    "fullname":fullname,
    "email":email,
    "username":username,
    "password":password,
    "is_active":is_active,
    "admin":admin,
}
    async def create_user2(user:UserSchemaCreate,db=Depends(get_async_session)):
        hashed_password =await users_crud.hash_password(user.password)
        passs=user.password
        passs= hashed_password
        result=await users_crud.create_user(db, user)
        
        return result
    output=await create_user2(UserSchemaCreate(**ex_user_create),db)
    error_msg=None
    if output==None:
        error_msg="There is another id with this username,please give a valid one"
        if error_msg:
            context={"request":request,"error_msg": error_msg}
            return templates.TemplateResponse("create_user.html", context=context)
    user=await users_crud.get_user_by_username(db,output.username)  
    output = UserSchema.from_orm(user)
    output=dict(output)
    user_schema_list = list(output.values())
    return templates.TemplateResponse("display_user.html",{"request":request,"users": user_schema_list})

    
    
@router.post("/token",response_model=Token|None,response_class=templates.TemplateResponse)
async def login_user(request:Request,form_data:OAuth2PasswordRequestForm=Depends(),db=Depends(get_async_session)):
    if form_data is None:
        return None

    if form_data.username == "":
        form_data.username = "===="
    if form_data.password == "":
        form_data.password = "===="
    db_user =await users_crud.get_user_by_username(db,form_data.username)
    print(db_user)
    error_msg=None
    if db_user is None:
        error_msg="This username not found"
     
    if error_msg:
        context={"request":request,"error_msg": error_msg}
        return templates.TemplateResponse("login.html", context=context)
    
    db_user2 =await users_crud.verify_password(form_data.password,db_user.hashed_password)
    if db_user2 is False:
        error_msg="This Password is not matching"
        
    if error_msg:
        context={"request":request,"error_msg": error_msg}
        return templates.TemplateResponse("login.html", context=context)

    payload = {"username": db_user.username, "role_is_admin:": db_user.admin}
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    save_username=await users_crud.save_username(db_user.username)
    save=await users_crud.save_token(token)
    context={"request":request}
    return templates.TemplateResponse("first_page.html",context=context)
    
    

@router.post("/update",response_class=templates.TemplateResponse,response_model=UserSchema,status_code=202,dependencies=[Depends(users_crud.check_admin)])

async def update_user(request:Request,id:int=Form(...),fullname:str=Form(...),email:str=Form(...),username:str=Form(...),password:str=Form(...),is_active:str=Form(...),admin:str=Form(...),db=Depends(get_async_session)):
    
    ex_user_create={
    "id":id,
    "fullname":fullname,
    "email":email,
    "username":username,
    "password":password,
    "is_active":is_active,
    "admin":admin,
    
}
    async def update_user2(user:UserSchema,db=Depends(get_async_session)):
        user=await users_crud.update_user(user.id,user,db)
        return user
    output=await update_user2(UserSchema(**ex_user_create),db)
    user=await users_crud.get_user_by_username(db,output.username)  
    output = UserSchema.from_orm(user)
    output=dict(output)
    user_schema_list = list(output.values())
    return templates.TemplateResponse("display_user.html",{"request":request,"users": user_schema_list})

@router.post("/delete",response_class=templates.TemplateResponse,status_code=200,dependencies=[Depends(users_crud.check_admin)])

async def delete_user(request: Request,id:int=Form(...),db=Depends(get_async_session)):
    user=await users_crud.delete_user(id,db)
    user=[id]
    context={"request":request,"user":user}
    return templates.TemplateResponse("display_delete.html",context=context)

@router.post("/update_me",response_class=templates.TemplateResponse,response_model=UserSchema,status_code=202,)

async def update_user(request:Request,id:int=Form(...),fullname:str=Form(...),email:str=Form(...),username:str=Form(...),password:str=Form(...),is_active:str=Form(...),admin:str=Form(...),db=Depends(get_async_session)):
    
    ex_user_create={
    "id":id,
    "fullname":fullname,
    "email":email,
    "username":username,
    "password":password,
    "is_active":is_active,
    "admin":admin,
    
}
    async def update_user2(user:UserSchemaCreate,db=Depends(get_async_session)):
        print(user.username)
        username=await users_crud.get_saved_username()
        username1=await users_crud.get_user_by_username(db,username) 
        print(username1.hashed_password)
        user=await users_crud.update_user_me(username1.id,user,db)
        return user
    output=await update_user2(UserSchemaCreate(**ex_user_create),db)
    user=await users_crud.get_user_by_username(db,output.username)  
    output = UserSchema.from_orm(user)
    output=dict(output)
    user_schema_list = list(output.values())
    return templates.TemplateResponse("display_user.html",{"request":request,"users": user_schema_list})
   