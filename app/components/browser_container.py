import flet as ft

class BrowserContainer(ft.Container):
    def __init__(self, content, **kwargs):
        super().__init__(**kwargs)
        self.content = content
        self.border = ft.border.all(1, ft.colors.WHITE)
        self.border_radius = ft.border_radius.all(10)
        self.padding = ft.padding.all(5)
