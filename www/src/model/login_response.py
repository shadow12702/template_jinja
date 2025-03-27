from datetime import datetime
from pydantic import BaseModel

class UserModel(BaseModel):
    Username: str
    Email: str
    LastIpAddress: str
    LastLoginDate: datetime

class TokenModel(BaseModel):
    access: str
    refresh: str
    
class LoginResponse(BaseModel):
    user: UserModel
    token: TokenModel

class RefreshTokenResponse(BaseModel):
    token: str

class MenuModel(BaseModel):
    code: str
    name: str
    icon: str = None
    parent: str = None
    route: str
    is_show : bool