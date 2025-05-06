from typing import Optional
from pydantic import BaseModel

class PatchRequest(BaseModel):
    id: int
    root: int
    db_version: str
    type: str
    format: str
    patch_type: str
    fixed_in_ru: Optional[str] = None
    fixed_in_mrp: Optional[str] = None
    description: Optional[str] = None