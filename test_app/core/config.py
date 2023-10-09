from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    #base connection
    api_v1_prefix:str
    debug:bool
    project_name:str
    version:str
    description:str
    db_async_connection_str:str
    db_async_connection_str:str
    
    
    