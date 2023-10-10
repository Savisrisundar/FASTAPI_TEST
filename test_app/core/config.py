from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    #base connection
    api_v1_prefix:str="/api/v1"
    debug:bool=True
    project_name:str="FASTAPI APP (local)"
    version:str="0.1.0"
    description:str="The API for FASTAPI app."
    db_async_connection_str:str="postgresql+asyncpg://postgres:Srihari1!@localhost:5432/Test_fastapi"
    db_sync_connection_str:str="postgresql+pg8000://postgres:Srihari1!@localhost:5432/Test_fastapi"
    templates:str="c:/Users/Sundark/Desktop/FASTAPI_TEST/test_app/templates"
    
    
    