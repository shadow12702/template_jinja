from apps.models.responses.menu_model import MenuModel
from core.request import RequestHandler

class MenuRepository():
    def get_menu(type: int):
        # Gọi API để lấy menu
        response = RequestHandler.post("/menu/get-menu", data={"type": type}, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            menu = [MenuModel(**item) for item in response.json()]
            # Process the menu to flag if an item has children
            for item in menu:
                item.has_children = any(child.parent == item.code for child in menu)
                if item.has_children:
                    item.route = None  
            return menu
        return []   