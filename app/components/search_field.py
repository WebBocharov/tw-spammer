from typing import Awaitable, Callable

import flet as ft

from app.components.browsers_listview import BrowsersListView


class SearchField(ft.TextField):
    def __init__(self, filter_func: Callable[[ft.ControlEvent], Awaitable], list_view: BrowsersListView, **kwargs):
        super().__init__(**kwargs)
        self.on_change = self.on_input
        self.filter_func = filter_func
        self.list_view = list_view

    async def on_input(self, event: ft.ControlEvent):
        filtered_data = await self.filter_func(event)
        await self.list_view.set_controls(filtered_data)
        self.list_view.update()
