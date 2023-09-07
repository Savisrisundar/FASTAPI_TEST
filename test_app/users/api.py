from fastapi import APIRouter, Depends
from test_app.core.db import get_async_session
from test_app.users.schemas import UserSchema,UserSchemaCreate
from test_app.users import crud as users_crud
router=APIRouter()

@router.get("/",response_model=list[UserSchema], status_code=200,)
async def get_users(db=Depends(get_async_session)):
    users=await users_crud.get_users(db)
    return users
@router.post("/", response_model=UserSchema, status_code=201,)
async def create_user(user:UserSchemaCreate,db=Depends(get_async_session)):
    user=await users_crud.create_user(db, user)
    return user