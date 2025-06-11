# Login Handler
from datetime import datetime
from typing import Callable, Any

from fastapi.openapi.utils import status_code_ranges
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi import Request, status, Query,Path
import uuid
from fs.fs import fs_open
from logic.core import user_model, security
from logic.DTO import user_dto
from logic.utils.db_dependency import get_db
from logic.core import security
from middleware import auth



async def login_handler(request: Request):
    body = await request.json()

    try:
        dto = user_dto.LoginDTO(**body)
    except Exception:
        return JSONResponse(
            content={"detail": "Invalid login data format"},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    db = next(get_db())
    user_result = user_model.get_user_by_username(db, dto.username)
    #print(user_result)
    if not user_result.success or user_result.data is None:
        return JSONResponse(
            content={"detail": "User not found"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    user = user_result.data  # Extract the actual User object

    # Verify password
    if not security.verify_password(dto.password, user.password_hash):
        return JSONResponse(
            content={"detail": "Invalid password"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    payload = {"user_id": user.id, "user_name": user.username, "role": user.role}
    access_token = auth.create_access_token(payload)
    refresh_token = auth.create_refresh_token(payload)

    response = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"},
        status_code=status.HTTP_200_OK
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=14 * 24 * 60 * 60,
        path="/api/v0.1/auth"
    )

    return response



# Token Refresh Handler
async def refresh_token_handler(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return JSONResponse(
            content={"detail": "Refresh token missing"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    payload = auth.decode_refresh_token(refresh_token)
    if not payload:
        return JSONResponse(
            content={"detail": "Invalid or expired refresh token"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    db = next(get_db())
    user_result = user_model.get_user_by_id(db,payload.get("user_id"))
    if not user_result.success or user_result.data is None:
        return JSONResponse(
            content={"detail": "User not found"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    user = user_result.data

    new_payload = {"user_id": user.id, "user_name": user.username, "role": user.role}
    new_access_token = auth.create_access_token(new_payload)
    new_refresh_token = auth.create_refresh_token(new_payload)

    response = JSONResponse(
        content={"access_token": new_access_token, "token_type": "bearer"},
        status_code=status.HTTP_200_OK
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=14 * 24 * 60 * 60,
        path="/api/v0.1/auth"
    )

    return response



# Register User (admin only)
async def register_user_handler(request: Request,user):
    try:
        body = await request.json()
        dto = user_dto.RegisterUserDTO(**body)
    except Exception:
        return JSONResponse(
            content={"detail": "Invalid registration data format"},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    if user.role != "admin":
        return JSONResponse(
            content={"detail": "Not authorized to register users"},
            status_code=status.HTTP_403_FORBIDDEN
        )
    db = next(get_db())
    new_user = {
        "full_name": dto.full_name.lower(),
        "username": dto.username.lower(),
        "email":dto.email.lower(),
        "role":dto.role.lower(),
        "password_hash":security.hash_password(dto.password),
        "created_at":datetime.utcnow(),
        "updated_at":datetime.utcnow()
    }
    result = user_model.create_user(db, new_user)

    if not result.success:
        return JSONResponse(
            content={"detail": result.error},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    response_dto = user_dto.UserResponseDTO.from_orm(result.data)
    return JSONResponse(
        content=response_dto.dict(),
        status_code=status.HTTP_201_CREATED
    )


# View own profile
async def view_profile_handler(request: Request, user):
    if user.role not in {"admin", "biller", "customer"}:
        return JSONResponse(
            content={"detail": "Invalid or unknown user"},
            status_code=status.HTTP_403_FORBIDDEN
        )

    db = next(get_db())
    result = user_model.get_user_by_id(db, user.id)

    if not result.success or not result.data:
        return JSONResponse(
            content={"detail": "User profile not found"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    response_dto = user_dto.UserResponseDTO.from_orm(result.data).dict()
    return JSONResponse(
        content=response_dto,
        status_code=status.HTTP_200_OK
    )
# Read user by ID (admin only): enables to retrieve specific customer or biller
async def read_user_by_id_handler(request: Request, user_id: str, user):
    if user.role != "admin":
        return JSONResponse(
            content={"detail": "Not authorized"},
            status_code=status.HTTP_403_FORBIDDEN
        )

    db = next(get_db())
    user_uuid = uuid.UUID(user_id)
    result = user_model.get_user_by_id(db, user_uuid)

    if not result.success or not result.data:
        return JSONResponse(
            content={"detail": "User not found"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    response_dto = user_dto.UserResponseDTO.from_orm(result.data).dict()
    return JSONResponse(
        content=response_dto,
        status_code=status.HTTP_200_OK
    )
async def update_user_by_id_handler(request: Request, user_id: str, user):
    try:
        body = await request.json()
        dto = user_dto.UpdateUserDTO(**body)
    except Exception:
        return JSONResponse(
            content={"detail": "Invalid update data format"},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    if user.role != "admin":
        return JSONResponse(
            content={"detail": "Not authorized"},
            status_code=status.HTTP_403_FORBIDDEN
        )

    db = next(get_db())
    user_uuid = uuid.UUID(user_id)
    result = user_model.update_user(db, user_uuid, dict(dto))

    if not result.success or not result.data:
        return JSONResponse(
            content={"detail": result.error or "User not found"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    response_dto = user_dto.UserResponseDTO.from_orm(result.data).dict()
    return JSONResponse(
        content=response_dto,
        status_code=status.HTTP_200_OK
    )


# Delete user by ID (admin only)
async def delete_user_by_id_handler(request: Request, user_id: str, user):
    if user.role != "admin":
        return JSONResponse(
            content={"detail": "Not authorized"},
            status_code=status.HTTP_403_FORBIDDEN
        )

    db = next(get_db())
    user_uuid = uuid.UUID(user_id)
    result = user_model.delete_user(db, user_uuid)

    if not result.success:
        return JSONResponse(
            content={"detail": result.error or "User not found"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    return JSONResponse(
        content={"detail": f"User with ID {user_uuid} deleted successfully."},
        status_code=status.HTTP_200_OK
    )
async def read_users_by_role_handler(request: Request, role: str, user):
    if user.role != "admin":
        return JSONResponse(
            content={"detail": "Not authorized"},
            status_code=status.HTTP_403_FORBIDDEN
        )

    valid_roles = {"admin", "customer", "biller"}
    if role not in valid_roles:
        return JSONResponse(
            content={"detail": f"Invalid role: {role}"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    db = next(get_db())
    result = user_model.get_users_by_role(db, role)

    if not result.success:
        return JSONResponse(
            content={"detail": result.error or "Could not fetch users"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    users = [user_dto.UserResponseDTO.from_orm(u).dict() for u in result.data]

    return JSONResponse(
        content={"users": users},
        status_code=status.HTTP_200_OK
    )
