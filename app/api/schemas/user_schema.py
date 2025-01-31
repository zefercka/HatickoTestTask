from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    user_id: int
    username: str
    email: str
    token: Optional[str]
    
    class Config:
        from_attributes = True