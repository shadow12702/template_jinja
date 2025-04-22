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


class CustomerResponse(BaseModel):
    cus_code: str
    cus_name: str

class AwrRepoInfoResponse(BaseModel):
    cus_code: str
    cus_name: str
    version: str
    db_name: str 
    cdb: str
    cdb_dbid: int
    pdb_dbid: int
    pdb_name: str
    min_snap: int
    min_time: str
    max_snap: int
    max_time: str

    