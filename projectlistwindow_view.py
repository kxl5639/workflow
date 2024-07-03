from view import ListWindow
from utils import center_window

class ProjectListWindow(ListWindow):
    def __init__(self, title, parent, controller, is_root=False):
        super().__init__(title, parent, controller, is_root)
