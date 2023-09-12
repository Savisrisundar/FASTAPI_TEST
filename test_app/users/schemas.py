from pydantic import BaseModel


from test_app.users.examples import ex_user_create,ex_user_read


class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    username:str|None=None
    

class UserSchemaBase(BaseModel):
    fullname:str
    email:str
    username:str
    admin:bool=True
    is_active:bool=False
    
class UserSchemaCreate(UserSchemaBase):
    password:str
    class Config:
        schema_extra={"example":ex_user_create}

class UserSchema(UserSchemaBase):
    id:int
    class Config:
        orm_mode=True
        schema_extra={"example":ex_user_read}
