from title_view import TitleView

class TitleController:
    def __init__(self, parent=None) -> None:
        self.parent = parent
        self.view = TitleView('Title Manager', self.parent, self)

    def add_entry(self, parent):
        self.view.create_entry_widget(parent)

    def moveup_entry(self):
        self.view.moveup_entry()

    def movedown_entry(self):
        self.view.movedown_entry()