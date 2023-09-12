from fastapi import APIRouter, Depends,HTTPException,status
from test_app.core.db import get_async_session
from test_app.users.models import User
from test_app.users.schemas import UserSchema,UserSchemaCreate,Token
from test_app.users import crud as users_crud
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
import jwt
from fastapi.security import OAuth2PasswordBearer
router=APIRouter()

JWT_SECRET="savi"
ALGORITHM="HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token/")

@router.get("/{username}",response_model=UserSchema|None, status_code=200,dependencies=[Depends(users_crud.check_admin)])
async def get_user(username:str,db=Depends(get_async_session)):
    print("Your details")
    #result=users_crud.check_crt_user
    #print(db_user)
    #print(password)
    print(username)
    #db_user =await users_crud.get_user_by_username(db,username)
   # db_user=await users_crud.get_password(db,username)
    
    #db_user1=await users_crud.verify_password(password,db_user)
   # if(db_user1 is True):
    user=await users_crud.get_user_by_username(db,username)
    
    return user
    
    
    """result=statement.admin
    if(result is True):
        final=await users_crud.get_users(db)
        return final
    else:
        #final=await users_crud.get_user_by_username(db,username)
        return statement"""
    """else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="unauthorized",)"""
    """if(db_user.admin is True):
        statement=await users_crud.get_users(db)
        
    else:
        statement=await users_crud.get_user_by_username(db,form_data.username)
    return statement"""
    
"""@router.get("/me",response_model=UserSchema|None, status_code=200)
async def get_me(user=Depends(users_crud.check_active_user)):
    return user"""

@router.post("/", response_model=UserSchema, status_code=201,dependencies=[Depends(users_crud.check_admin)])

async def create_user(user:UserSchemaCreate,db=Depends(get_async_session)):
    hashed_password =await users_crud.hash_password(user.password)
    user.password = hashed_password
    """db_user=users_crud.get_users(db,username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="email already registered")"""
    result=await users_crud.create_user(db, user)
    return result
@router.post("/token", response_model=Token)
async def login_user(form_data:OAuth2PasswordRequestForm=Depends(),db=Depends(get_async_session)):
    db_user =await users_crud.get_user_by_username(db,form_data.username)
    print(db_user)
    if db_user is None:
        raise HTTPException(
        status_code=401, detail="This username not found"
    )
    test=await users_crud.get_password(db,form_data.username)
    print(test)
    db_user2 =await users_crud.verify_password(form_data.password,db_user.hashed_password)
    print(db_user2)
    if db_user2 is False:
        raise HTTPException(status_code=401, detail="password not matched")

    payload = {"username": db_user.username, "role_is_admin:": db_user.admin}
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}
        

@router.put("/{id}",response_model=UserSchema,status_code=202,dependencies=[Depends(users_crud.check_admin)])
async def update_user(id:int,todos:UserSchema,db=Depends(get_async_session)):
    user=await users_crud.update_user(id,todos,db)
    return user

@router.delete("/{id}",status_code=200,dependencies=[Depends(users_crud.check_admin)])

async def delete_user(id:int,db=Depends(get_async_session)):
    user=await users_crud.delete_user(id,db)
    return user