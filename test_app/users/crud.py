from sqlalchemy import select
from test_app.core.db import get_async_session
from fastapi import Depends,HTTPException,status
import bcrypt
from sqlalchemy.orm import Session
from test_app.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from test_app.users.schemas import UserSchema,UserSchemaCreate
from passlib.context import CryptContext
import jwt
from fastapi.security import OAuth2PasswordBearer


JWT_SECRET="savi"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token/")


async def get_user_by_username(db:AsyncSession,username:str):
    statement = select(User).where(User.username==username)
    result= await db.execute(statement)
    user=result.scalars().one_or_none()
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
    """Verifies a password against a hashed password."""
    #return pwd_context.verify(password, hashed_password)
    
    if(password==hashed_password):
        return True
    else:
        return False
    

async def hash_password(password:str):
    print(password)
    return password

async def get_users(db: AsyncSession):
    statement = select(User)
    result= await db.execute(statement)
    users=result.scalars().all()
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
    

    await db.commit()

    return user_in_db

async def delete_user(id:int,db:AsyncSession):
    
    user = await db.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="Todo not found")

    await db.delete(user)
    await db.commit()

    return user

"""async def verify_password(plain_pass,hashed_pass):
    return pwd_context.verify(plain_pass,hashed_pass)"""

async def verify_token(token):
    try:
        payload=jwt.decode(token,key=JWT_SECRET,algorithms=ALGORITHM)
        return payload
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="token is not valid",
                            headers={"WWW-Authenticate":"Bearer"},)
    
async def check_active(token:str=Depends(oauth2_scheme)):
    payload=await verify_token(token)
    print("payload:",payload)
    async def get_payload(payload):
        return dict(payload)
    payload = await get_payload(payload)
    active=payload.get('role_is_admin:')
    active1=payload.get('username')
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
async def check_active_user(token:str=Depends(oauth2_scheme),db=Depends(get_async_session)):
    payload=await verify_token(token)
    username=payload.get("username")
    user=await get_user_by_username(db,username)
    if user.is_active==True:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="use is not active",)

async def check_crt_user(payload: bool = Depends(check_active_user)):
    
    print(payload)
    
    return payload
        
    

    
