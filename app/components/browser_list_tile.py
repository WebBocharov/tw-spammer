import asyncio

import flet as ft

from app.components.modals import AddGroupsUrlModalView
from database.models import BrowserProfile


class BrowserListTile(ft.ListTile):
    def __init__(self, browser: BrowserProfile, **kwargs):
        super().__init__(**kwargs)
        self.title = ft.Text()
        self.browser = browser
        self.subtitle = ft.Text(self.browser.browser_id)
        self.leading = ft.Switch(value=False, disabled=True, width=50)
        self.shape = ft.RoundedRectangleBorder(radius=5)
        self.modal = AddGroupsUrlModalView(self.browser)
        self.on_click = lambda e: self.page.open(self.modal)
        self.data = f"{self.browser.id}"

        asyncio.create_task(self.set_title())

    async def set_title(self):
        title_text = await self.generate_title()
        self.title.value = title_text
        self.update()

    async def generate_title(self):
        return f"{self.browser.serial_number}. {self.browser.name} ({await self.browser.twitter_group_urls.all().count()})"
