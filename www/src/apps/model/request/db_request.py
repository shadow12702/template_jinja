# database-request.py

from pydantic import BaseModel

class DbRequest(BaseModel):
    """
    Model for database request.
    """
    customer_code: str
    dbid: int
    begin_snap: int
    end_snap: int
    is_rac: bool = False
    is_exa: bool = False
    is_cdb: bool = False
    
    