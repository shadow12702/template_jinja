from datetime import datetime, timedelta
import re
from typing import Any, Dict

class AppHelper:
        
    def strNotEmpty(self, s: str) -> bool:        
        'Check string is not empty'
        return bool(s and s.strip())

    def emailValid(self, email:str):
        '''Check email format'''
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(pattern, email)) or not self.strNotEmpty(email)

    @staticmethod
    def map_keys(current_dict, key_mapping):
        """Map dictionary keys to match target structure using a mapping dictionary."""
        mapped_dict = {}
        for section, mappings in key_mapping.items():
            mapped_dict[section] = {} 
            for old_key, new_key in mappings.items():
                if old_key in current_dict.get(section, {}): 
                    value = current_dict[section][old_key]
                    mapped_dict[section][new_key] = value
        return mapped_dict

    @staticmethod
    def to_nested_dict(data: Dict[str, Any], split_str: str = '.') -> Dict[str, Any]:
        """Convert a dot-key dictionary into a nested dictionary"""
        nested = {}
        for key, value in data.items():
            keys = key.split(split_str)
            d = nested
            for k in keys[:-1]:  
                d = d.setdefault(k, {})
            d[keys[-1]] = value  
        return nested

    @staticmethod
    def flatten_dict(d, parent_key:str='', sep:str='.'):
        """Flatten a nested dictionary and concatenate keys."""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict): 
                items.extend(AppHelper.flatten_dict(v, new_key, sep=sep).items())
            else: 
                items.append((new_key, v))
        return dict(items)
    
    @staticmethod
    def get_date_utc(delta: int=0) -> str:    
        'Get UTC date '
        _format = "%d/%m/%Y %H:%M:%S"            
        date = (datetime.utcnow() + timedelta(minutes=delta)).strftime(_format)
        return date

helper = AppHelper()