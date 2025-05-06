# refresh_token_response.py

from pydantic import BaseModel

class RefreshTokenResponse(BaseModel):
    token: str