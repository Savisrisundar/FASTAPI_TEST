from sqlalchemy import select
from test_app.core.db import get_async_session
from fastapi import Depends,HTTPException,status
import bcrypt
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from test_app.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from test_app.users.schemas import UserSchema,UserSchemaCreate
from passlib.context import CryptContext
import jwt
from fastapi.security import OAuth2PasswordBearer
from test_app.users import api
templates=Jinja2Templates(directory="c:/Users/Sundark/Desktop/FASTAPI_TEST/test_app/templates")
JWT_SECRET="savi"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token/")
access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InNhdml0aGEiLCJyb2xlX2lzX2FkbWluOiI6dHJ1ZX0.C5Eyd9sspMx1rPSc1pDc-C3zcn6dBuWH8HYJ2_1nkeo"
token_val=""
async def get_user_by_username(db:AsyncSession,username:str):
    statement = select(User).where(User.username==username)
    result= await db.execute(statement)
    user=result.scalars().one_or_none()
    print("users are:",user)
    return user
    

async def get_password(db,username):
    user = await get_user_by_username(db, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="unauthorized",)
    print(user.username)
    return user.hashed_password
    

async def verify_password(password:str, hashed_password:str):
    if(password==hashed_password):
        return True
    else:
        return False
    

async def hash_password(password:str):
    print(password)
    return password

async def get_users(db: AsyncSession):
    statement = select(User)
    result = await db.execute(statement)
    users = result.scalars().all()
    return users


async def authenticate_user(db:AsyncSession,username:str,password:str):
    user=await db.get(User.username,username)
    if not user:
        return False
    user1=await db.get(User.hashed_password,username)
    if not verify_password(password,user1):
        return False
    
    return user

async def create_user(db:AsyncSession, user:UserSchemaCreate):
    hash_password=user.password
    del user.password
    statement=await get_users(db)
    for use in statement:
        if use.username==user.username:
            return None
        elif use.email==user.email:
            return None
    db_user=User(**user.dict())
    db_user.hashed_password=hash_password
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(id:int,user:UserSchema,db:AsyncSession):
    user_in_db = await db.get(User, id)
    if not user_in_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    user_in_db.fullname = user.fullname
    user_in_db.username = user.username
    user_in_db.email=user.email
    user_in_db.is_active=user.is_active
    user_in_db.admin=user.admin
    await db.commit()
    return user_in_db

async def update_user_me(id:int,user:UserSchemaCreate,db:AsyncSession):
    user_in_db = await db.get(User, id)
    if not user_in_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_in_db.fullname = user.fullname
    user_in_db.username = user.username
    user_in_db.email=user.email
    user_in_db.hashed_password=user.password
    user_in_db.is_active=user.is_active
    user_in_db.admin=user.admin
    await db.commit()
    return user_in_db

async def delete_user(id:int,db:AsyncSession):
    user = await db.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return user

async def save_token(token:str):
    global token_val
    token_val=token
    print(token)
    return token_val

async def get_saved_token():
    print(token_val)
    return token_val


async def save_username(username:str):
    global string
    string=username
    return string

async def get_saved_username():
    print(string)
    return string

async def get_user_by_id(id:int,db:AsyncSession):
    todo = await db.get(User, id)
    return todo

async def verify_token(token):
    try:
        payload=jwt.decode(token,key=JWT_SECRET,algorithms=ALGORITHM)
        return payload
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="token is not valid",
                            headers={"WWW-Authenticate":"Bearer"},)
    
async def check_active(token:str=Depends(get_saved_token)):
    payload=await verify_token(token)
    print("payload:",payload)
    async def get_payload(payload):
        return dict(payload)
    payload = await get_payload(payload)
    active=payload.get('role_is_admin:')
    active1=payload.get('username')
    users1=await save_username(active1)
    print(active1)
    print(active)
    if not active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="this is accessible only by admins",
                            headers={"WWW-Authenticate":"Bearer"},)
    else:
        return active
    
async def check_admin(payload: bool = Depends(check_active)):
    print("payload", payload)
    return payload

async def check_active_user(token:str=Depends(oauth2_scheme)):
    payload=await verify_token(token)
    username=payload.get("username")
    users1=await save_username(username)
    return users1
        

        
    

    
