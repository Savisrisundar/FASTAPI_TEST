from fastapi import APIRouter
from test_app.users.schemas import UserSchema
router=APIRouter()

@router.get("/",response_model=list[UserSchema], status_code=200,)
async def get_users():
    