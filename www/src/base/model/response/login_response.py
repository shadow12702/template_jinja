# login_response.py

from pydantic import BaseModel

from base.model.token_model import TokenModel
from base.model.user_model import UserModel

class LoginResponse(BaseModel):
    user: UserModel
    token: TokenModel