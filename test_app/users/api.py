from fastapi import APIRouter, Depends,HTTPException,Request,status
from fastapi.templating import Jinja2Templates
import requests
from fastapi.responses import RedirectResponse
from test_app.core.db import get_async_session
from test_app.users.models import User
from test_app.users.schemas import UserSchema,UserSchemaCreate,Token
from test_app.users import crud as users_crud
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
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


@router.get("/me",response_model=UserSchema, status_code=200,dependencies=[Depends(users_crud.check_admin)])

async def get_me(db=Depends(get_async_session)):
    
    username=await users_crud.get_saved_username()
    username1=await users_crud.get_user_by_username(db,username)
    return username1


@router.get("/username",response_model=UserSchema|None, status_code=200,dependencies=[Depends(users_crud.check_admin)])

async def get_user(username:str,db=Depends(get_async_session)):
    print("Your details")   
    print(username) 
    user=await users_crud.get_user_by_username(db,username)    
    return {"users": user}
    #return templates.TemplateResponse("users.html", context=context)
     





@router.post("/", response_model=UserSchema, status_code=201,dependencies=[Depends(users_crud.check_admin)])

async def create_user(user:UserSchemaCreate,db=Depends(get_async_session)):
    hashed_password =await users_crud.hash_password(user.password)
    user.password = hashed_password
    
    result=await users_crud.create_user(db, user)
    return result

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
    save=await users_crud.save_token(token)
    #return {"access_token": token, "token_type": "bearer"}
    #return RedirectResponse(url=fastapi_app.url_path_for("home"),status_code=status.HTTP_303_SEE_OTHER)
    context={"request":request}
    return templates.TemplateResponse("users.html",context=context)
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