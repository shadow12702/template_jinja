import json
import os
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from core.enum.app_enum import AppEnum
from core.helper import helper

class BaseModel:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if isinstance(v, dict):
                model_class = getattr(self.__class__, "__annotations__",{}).get(k)
                if model_class:
                    v = model_class(**v) 
                else:
                    v = BaseModel(**v)
            setattr(self, k, v)

class AppConfig:
    '''Application settings'''
    _instance = None
        
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance._load()
            cls._instance._json_hot_reload()
        return cls._instance
        
    def _load(self):
        '''Config loading '''
        with open(AppEnum.JSON_CONFIG.file_path, "r") as js_file:
            config_json = json.load(js_file)        
        self.config = self._load_json(config_json)
        
    def _load_json(self, js_config):
        js_data = helper.to_nested_dict({k: helper.to_nested_dict(v) if isinstance(v, dict) else v 
                                                for k, v in js_config.items()})
        flat_js = helper.flatten_dict(js_data)
        js_data.update({"apiUrl": f"{flat_js['api_url.host']}:{flat_js['api_url.port']}" if isinstance(flat_js.get('api_url.port'), int) else flat_js['api_url.host']})
        return BaseModel(**js_data)
        
    def _json_hot_reload(self):
        '''Set up hot-reload when config.json has been changed'''
        event_handler = ConfigFileChangeHandler(self, AppEnum.JSON_CONFIG.file_path)
        observer = Observer()
        observer.schedule(event_handler, 
                          path= os.path.dirname(AppEnum.JSON_CONFIG.file_path),
                          recursive=False)


class ConfigFileChangeHandler(FileSystemEventHandler):
    """Reload config when file INI changed"""
    def __init__(self, config_loader: AppConfig, cf_file: str):
        self.config_loader = config_loader
        self.config_file = cf_file

    def on_modified(self, event):
        if event.src_path == self.config_file:
            print("Detected change in config file. Reloading...")
            self.config_loader._load_config()



app_config = AppConfig().config