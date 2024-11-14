import flet as ft

from app.components.modals import AddGroupsUrlModalView
from database.models import BrowserProfile


class BrowserListTile(ft.ListTile):
    def __init__(self, browser: BrowserProfile, **kwargs):
        super().__init__(**kwargs)
        self.title = ft.Text(browser.serial_number + ". " + browser.name)
        self.subtitle = ft.Text(browser.browser_id)
        self.leading = ft.Switch(value=False, disabled=True, width=50)
        self.shape = ft.RoundedRectangleBorder(radius=5)
        self.modal = AddGroupsUrlModalView(browser)
        self.on_click = lambda e: self.page.open(self.modal)
        self.data = f"{browser.id}"
