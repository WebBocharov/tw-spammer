from typing import Callable

import flet as ft


class StopSpamButton(ft.ElevatedButton):
    def __init__(self, callback: Callable, **kwargs):
        super().__init__(**kwargs)
        self.text = "Зупинити розсилку"
        self.callback_function = callback
        self.on_click = self.click_callback

    async def click_callback(self, event: ft.ControlEvent):
        await self.callback_function(event)
