# backend/app/models/user.py
from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    roles: List[str] = []
