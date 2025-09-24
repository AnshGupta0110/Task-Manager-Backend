from pydantic import BaseModel
from typing import List, Optional

# ------------------ User Schemas ------------------
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    tasks: List["TaskResponse"] = []  # Forward reference

    class Config:
        orm_mode = True

# ------------------ Task Schemas ------------------
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True

# ------------------ Auth / Login ------------------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# ------------------ Fix forward references ------------------
UserResponse.update_forward_refs()

