# 

from pydantic import BaseModel

class MenuModel(BaseModel):
    code: str
    name: str
    icon: str = None
    parent: str = None
    has_children: bool = False
    admin: int = 0
    route: str
    is_show : bool

