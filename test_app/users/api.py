from fastapi import APIRouter, Depends,HTTPException,Request,status,Form
from fastapi.templating import Jinja2Templates
import requests
import json
from fastapi.responses import RedirectResponse
from test_app.core.db import get_async_session
from test_app.users.models import User
from test_app.users.schemas import UserSchema,UserSchemaCreate,Token,UserSchemaBase
from test_app.users import crud as users_crud
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
import jwt
from pydantic import BaseModel

from fastapi.security import OAuth2PasswordBearer
templates=Jinja2Templates(directory="c:/Users/Sundark/Desktop/FASTAPI_TEST/test_app/templates")
router=APIRouter()

JWT_SECRET="savi"
ALGORITHM="HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token/")
payloads={}
def get_pays():
    return payloads
def pydantic_encoder(obj):
        if isinstance(obj, BaseModel):
            return obj.dict()
        return json.JSONEncoder.default(obj)


@router.get("/me",response_model=UserSchema, status_code=200)

async def get_me(request:Request,db=Depends(get_async_session)):
    
    username=await users_crud.get_saved_username()
    username1=await users_crud.get_user_by_username(db,username)
    user_schema = UserSchema.from_orm(username1)
    user_schema=dict(user_schema)
    user_schema_list = list(user_schema.values())
    print(user_schema)
    #return username1
    return templates.TemplateResponse("display_user.html",{"request":request,"users": user_schema_list})


@router.get("/username",response_model=UserSchema|None|dict, status_code=200,dependencies=[Depends(users_crud.check_admin)])

async def get_user(request:Request,username:str,db=Depends(get_async_session)):
    print("Your details")   
    print(username) 
    user=await users_crud.get_user_by_username(db,username)    
    print("username:",user.username)
    
    user_schema = UserSchema.from_orm(user)
    user_schema=dict(user_schema)
    user_schema_list = list(user_schema.values())
    print(user_schema)
    #print(user_schema)
    #return user_schema
    #return {"users":"savitha"}
    #return {"users": user.username}
    #return templates.TemplateResponse("users.html", context=context)
   
    """user_schema_json = json.dumps(user_schema,default=pydantic_encoder)
    context = {"request":request,"users": user_schema_json}
    print(context)"""
    return templates.TemplateResponse("display_user.html",{"request":request,"users": user_schema_list})
"""async def convert_to_list(request:Request):
    user_data_list=json.dumps([request.form.__get__("id"),
                               request.form.__get__("fullname"),
                               request.form.__get__("email"),
                               request.form.__get__("username"),
                               request.form.__get__("password"),
                               request.form.__get__("is_active"),
                               request.form.__get__("admin"),])
    user_data_list=json.loads(request.form.__get__("user_data_list"))
    return user_data_list"""
    




@router.post("/create",response_model=UserSchema, response_class=templates.TemplateResponse, status_code=201,dependencies=[Depends(users_crud.check_admin)])

async def create_user(request:Request,id:int=Form(...),fullname:str=Form(...),email:str=Form(...),username:str=Form(...),password:str=Form(...),is_active:bool=Form(...),admin:bool=Form(...),db=Depends(get_async_session)):
    """user_json = await request.json()
    user = UserSchemaCreate.from_dict(json.loads(user_json))"""
    #user.id = str(user.id)
    print(fullname)
    fullname=fullname
    email=email
    username=username
    password=password
    is_active=is_active
    admin=admin
    ex_user_create={
    
    "fullname":fullname,
    "email":email,
    "username":username,
    "password":password,
    "is_active":is_active,
    "admin":admin,
    
}
    async def create_user2(user:UserSchemaCreate,db=Depends(get_async_session)):
      
        hashed_password =await users_crud.hash_password(user.get("password"))
        passs=user.get("password")
        passs= hashed_password
        result=await users_crud.create_user(db, user)
        return result
    output=await create_user2(ex_user_create,db)
    return output
    
    
    

@router.post("/token",response_model=Token,response_class=templates.TemplateResponse)

async def login_user(request:Request,form_data:OAuth2PasswordRequestForm=Depends(),db=Depends(get_async_session)):
    db_user =await users_crud.get_user_by_username(db,form_data.username)
    
    print(db_user)
    
    #string=db_user.username
    #print(string)
    if db_user is None:
        raise HTTPException(
        status_code=401, detail="This username not found"
    )
    db_user2 =await users_crud.verify_password(form_data.password,db_user.hashed_password)
    if db_user2 is False:
        raise HTTPException(status_code=401, detail="password not matched")

    payload = {"username": db_user.username, "role_is_admin:": db_user.admin}
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    #global payloads
    # payloads=token
    save_username=await users_crud.save_username(db_user.username)
    save=await users_crud.save_token(token)
    #return {"access_token": token, "token_type": "bearer"}
    #return RedirectResponse(url=fastapi_app.url_path_for("home"),status_code=status.HTTP_303_SEE_OTHER)
    if db_user.admin is True:
        context={"request":request}
        return templates.TemplateResponse("users.html",context=context)
    else:
        context={"request":request}
        return templates.TemplateResponse("users_not_admin.html",context=context)
"""@router.get("/get_token",response_model=Token)
async def save_payload():
    global payloads
    payload=payloads
    return payload"""

    

@router.put("/{id}",response_model=UserSchema,status_code=202,dependencies=[Depends(users_crud.check_admin)])

async def update_user(id:int,todos:UserSchema,db=Depends(get_async_session)):
    user=await users_crud.update_user(id,todos,db)
    return user

@router.delete("/{id}",status_code=200,dependencies=[Depends(users_crud.check_admin)])

async def delete_user(id:int,db=Depends(get_async_session)):
    user=await users_crud.delete_user(id,db)
    return user