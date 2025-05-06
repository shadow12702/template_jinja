# admin/model/response/config_response.py

from pydantic import BaseModel

class ConfigResponse(BaseModel):
    ''' A class to represent the response of a configuration. '''
    
    type: str
    key: str
    value: str
    is_locked: int
