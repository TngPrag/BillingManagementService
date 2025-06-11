from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class LoginDTO(BaseModel):
    username: str = Field(..., example="admin")
    password: str = Field(..., min_length=6, example="password")


class RegisterUserDTO(BaseModel):
    full_name: str = Field(..., example="John Doe")
    username: str = Field(..., example="johndoe")
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., min_length=6, example="password")
    role: str = Field(..., example="biller")  # consider enum later


class UpdateUserDTO(BaseModel):
    full_name: Optional[str] = Field(None, example="John Doe")
    username: Optional[str] = Field(None, example="johndoe")
    email: Optional[EmailStr] = Field(None, example="john@example.com")
    role: Optional[str] = Field(None, example="biller")


class UserResponseDTO(BaseModel):
    id: str
    full_name: str
    username: str
    email: EmailStr
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # allows parsing from ORM models directly
