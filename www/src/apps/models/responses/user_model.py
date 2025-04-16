# 


from datetime import datetime
from pydantic import BaseModel


class UserModel(BaseModel):
    Username: str
    Email: str
    LastIpAddress: str
    LastLoginDate: datetime