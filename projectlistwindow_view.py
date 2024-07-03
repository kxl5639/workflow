from view import BaseWindow
class ProjectAddModifyWindow(BaseWindow):
    def __init__(self, title, parent, is_root=False, is_modify=False):
        super().__init__(title, parent.root, is_root)        
        self.title = title
        self.parent = parent
        self.is_modify = is_modify
        self.tree = self.parent.tree_frame.tree


        BaseWindow.center_window(self.root)
    

        

        
        


        
        