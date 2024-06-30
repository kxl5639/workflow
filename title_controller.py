from title_view import TitleView

class TitleController:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.view = TitleView('Title Manager', self.parent, self)

    def add_entry(self, parent):
        self.view.create_entry_widget(parent)