from typing import List

import flet as ft

from database.models import BrowserProfile
from .browser_container import BrowserContainer
from .browser_list_tile import BrowserListTile


class BrowsersListView(ft.ListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width = 400
        self.height = 400
        self.spacing = 5
        self.expand = True

    async def set_controls(self, browsers: List[BrowserProfile]):
        self.controls.clear()
        self.controls = [BrowserContainer(BrowserListTile(browser)) for browser in browsers]
        return self

    async def update_status(self, browser_id: str):
        for control in self.controls:
            if control.content.data == browser_id:
                control.content.leading.value = not control.content.leading.value
        self.update()
        return self
