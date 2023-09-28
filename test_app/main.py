from fastapi import FastAPI,Request,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
#from fastapi import APIRouter as api_router
from test_app import settings
from test_app.core.models import HealthCheck
from test_app.router.endpoints import api_router
from fastapi.staticfiles import StaticFiles
templates=Jinja2Templates(directory="c:/Users/Sundark/Desktop/FASTAPI_TEST/test_app/templates")
fastapi_app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    debug=settings.debug,
    templates="templates",
    #security={},
)
#fastapi_app.mount("/static",StaticFiles(directory="static"),name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token/")

@fastapi_app.get("/")
async def home(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})

@fastapi_app.get("/login", response_class=templates.TemplateResponse)
async def login_form(request: Request):
  #context={"request":request.cookies.get("access_token")}
  context = {"request": request}
  return templates.TemplateResponse("login.html",context=context)
  #return RedirectResponse(url=fastapi_app.url_path_for("get_user"),status_code=status.HTTP_303_SEE_OTHER)

@fastapi_app.get("/user", response_class=templates.TemplateResponse)

async def get_user(request:Request):
    context={"request":request}
    #access_token = request.cookies.get("access_token")
    return templates.TemplateResponse("users.html",context=context)





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

