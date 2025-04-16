# 

from pydantic import BaseModel

class AwrRepoInfoResponse(BaseModel):
    customer_code: str
    customer_name: str
    version: str
    db_name: str 
    cdb: str
    cdb_dbid: int
    pdb_dbid: int
    pdb_name: str
    begin_snap: int
    begin_time: str
    end_snap: int
    end_time: str

    