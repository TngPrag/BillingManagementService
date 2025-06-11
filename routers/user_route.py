from fastapi import APIRouter, Depends,Request
from logic.handlers.user_handler import (
    login_handler,
    refresh_token_handler,
    register_user_handler,
    view_profile_handler,
    read_user_by_id_handler,
    update_user_by_id_handler,
    delete_user_by_id_handler,
    read_users_by_role_handler,
)
from middleware.auth import get_current_user  # Auth dependency


user_routes = APIRouter(
    prefix="/api/v0.1/auth",
    tags=["Auth / Users"]
)

# Public endpoints
@user_routes.post("/login")
async def login(request: Request):
    return await login_handler(request)

@user_routes.get("/refresh-token")
async def refresh_token(request: Request):
    return await refresh_token_handler(request)

# Protected endpoints
@user_routes.post("/register")
async def register_user(request: Request,user = Depends(get_current_user)):
    return await register_user_handler(request,user)

@user_routes.get("/me")
async def view_profile(request: Request, user = Depends(get_current_user)):
    return await view_profile_handler(request,user)

@user_routes.get("/users/{user_id}")
async def read_user_by_id(request: Request,user_id: str, user = Depends(get_current_user)):
    return await read_user_by_id_handler(request,user_id, user)

@user_routes.put("/users/{user_id}")
async def update_user_by_id(request: Request,user_id: str, user = Depends(get_current_user)):
    return await update_user_by_id_handler(request,user_id, user)

@user_routes.delete("/users/{user_id}")
async def delete_user_by_id(request: Request,user_id: str, user= Depends(get_current_user)):
    return await delete_user_by_id_handler(request,user_id, user)

@user_routes.get("/users/by-role")
async def read_users_by_role(user= Depends(get_current_user)):
    return await read_users_by_role_handler(user)
