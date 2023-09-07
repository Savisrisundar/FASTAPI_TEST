from sqlalchemy import select
from test_app.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from test_app.users.schemas import UserSchema,UserSchemaCreate
async def get_users(db: AsyncSession):
    statement = select(User)
    result= await db.execute(statement)
    users=result.scalars().all()
    return users

async def create_user(db:AsyncSession, user:UserSchemaCreate):
    hash_password=user.password
    
    #pop out user from password
    del user.password
    db_user=User(**user.dict())
    db_user.hashed_password=hash_password
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
