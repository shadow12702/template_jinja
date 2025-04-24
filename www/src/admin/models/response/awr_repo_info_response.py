# 
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AwrRepoInfoResponse(BaseModel):
    customer_code: str
    customer_name: str
    version: str 
    db_name: str
    cdb: bool
    pdb_dbid: int 
    pdb_name: str 
    end_snap: Optional[int] = None
    end_time: Optional[datetime] = None


    