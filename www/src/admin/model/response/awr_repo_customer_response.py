# admin/model/response/awr_repo_customer_response.py

from datetime import datetime
from pydantic import BaseModel

class AwrRepoCustomerResponse(BaseModel):
    dbid: int = 0
    database_name: str
    version: str
    is_cdb: bool = False
    begin_snap: int
    begin_time: datetime
    end_snap: int
    end_time: datetime
    is_rac: bool = False
    is_exa: bool = False
    block_size: int
    