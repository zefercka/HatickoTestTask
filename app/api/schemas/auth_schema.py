from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class Authorization(BaseModel):
    login: Annotated[str, Field(min_length=4, max_length=256)]
    password: Annotated[str, Field(min_length=8, max_length=32)]


class Registration(BaseModel):
    username: Annotated[str, Field(min_length=4, max_length=16)]
    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=32)]