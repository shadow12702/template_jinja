# menu_service.py

from base.model.menu_model import MenuModel
from core.request import RequestHandler

def get_menu(type: int = 0):
    """
    Fetches the menu from the server and updates the session.
    """
    response = RequestHandler.post('/menu/get-menu', data={"type": type}, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        menu_data = response.json()
        menu = [MenuModel(**item) for item in menu_data] 
        for mnu in menu:
            mnu.admin = type
            mnu.has_children = any(child.parent == mnu.code for child in menu)
            if mnu.has_children:
                mnu.route = None                    
        return menu
    return None

