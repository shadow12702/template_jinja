from enum import Enum
from pathlib import Path

ROOT_AT = 'src'
class AppEnum(Enum):
    
    # Config file    
    JSON_CONFIG = 'config/bk.config.json'
        
    @property
    def file_path(self):
        current_path = Path(__file__).parent
        index = current_path.parts.index(ROOT_AT)
        base_path = Path(*current_path.parts[:index+1])
        path = (base_path/self.value).resolve()
        return path
        
    