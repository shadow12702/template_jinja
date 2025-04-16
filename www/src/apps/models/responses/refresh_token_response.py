
from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    token: str

