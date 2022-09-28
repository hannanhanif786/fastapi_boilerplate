from pydantic import BaseModel, EmailStr
from typing import List, Union


class CreateUserIn(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    is_active: bool


class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_no: str


class UpdateUser(BaseModel):
    name: str
    phone_no: str


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    phone_no: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class changepassword(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str


class ForgetPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    password: str
    confirm_password: str
