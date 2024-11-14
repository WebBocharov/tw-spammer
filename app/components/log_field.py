import flet as ft


class LogField(ft.TextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = ""
        self.label = "Логи"
        self.multiline = True
        self.read_only = True
        self.expand = True
        self.max_lines = 500
        self.border_color = ft.colors.WHITE
        self.border_radius = ft.border_radius.all(10)

    async def write(self, message: str):
        if len(self.value.split("\n")) > self.max_lines:
            self.value = ""
        self.value = message + "\n" + self.value
        self.update()
