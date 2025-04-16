from datetime import datetime
from pydantic import BaseModel

from apps.models.responses.token_model import TokenModel
from apps.models.responses.user_model import UserModel

class LoginResponse(BaseModel):
    user: UserModel
    token: TokenModel
