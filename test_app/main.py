from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm


#from fastapi import APIRouter as api_router
from test_app import settings
from test_app.core.models import HealthCheck
from test_app.router.endpoints import api_router
fastapi_app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    debug=settings.debug,
    #security={},
)

fastapi_app.include_router(api_router, prefix=settings.api_v1_prefix)
@fastapi_app.on_event("startup")
async def app_startup():
    print("app started")
    
@fastapi_app.on_event("shutdown")
async def pickle_schedule():
    print("app shut down")
    
@fastapi_app.get("/",response_model=HealthCheck, tags=["status"])
async def health_check():
    return{
        "name":settings.project_name,
        "version":settings.version,
        "description":settings.description
    }    

