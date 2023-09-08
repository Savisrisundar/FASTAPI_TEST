from fastapi import APIRouter
from test_app.users.api import router as users_router
from test_app.todos.api import router as todos_router
api_router= APIRouter()
include_api= api_router.include_router
routers=((users_router,"users","users"),(todos_router,"todos","todos"),)

for router_item in routers:
    router, prefix, tag =router_item
    
    if tag:
        include_api(router, prefix =f"/{prefix}",tags=[tag])
    else:
        include_api(router,prefix="f/{prefix}")
        