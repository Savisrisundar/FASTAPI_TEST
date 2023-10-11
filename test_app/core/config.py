from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    #base connection
    api_v1_prefix:str="/api/v1"
    debug:bool=True
    project_name:str="FASTAPI APP (local)"
    version:str="0.1.0"
    description:str="The API for FASTAPI app."
    db_async_connection_str:str="postgresql+asyncpg://postgres_k2ef_user:Sn1buHBLyd8En2VEskq3pGftVkn84UcA@dpg-ckj2sk8lk5ic73bmkd10-a.oregon-postgres.render.com/postgres_k2ef"
    db_sync_connection_str:str="postgresql+pg8000://postgres_k2ef_user:Sn1buHBLyd8En2VEskq3pGftVkn84UcA@dpg-ckj2sk8lk5ic73bmkd10-a.oregon-postgres.render.com/postgres_k2ef"
    
    
    
    