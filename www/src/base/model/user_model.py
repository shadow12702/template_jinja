#  user_model.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserModel(BaseModel):
    username: str
    email: Optional[str] = "user@orapy.com"
    is_admin: bool = False
    last_ip_address: str
    last_login_date: datetime