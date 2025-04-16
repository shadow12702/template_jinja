# 


from pydantic import BaseModel


class TokenModel(BaseModel):
    access: str
    refresh: str