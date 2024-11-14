import flet as ft

from database.controllers import BrowserProfileController, TwitterGroupUrlController
from database.models import BrowserProfile, TwitterGroupUrl


class AddGroupsUrlModalView(ft.AlertDialog):
    def __init__(self, browser: BrowserProfile, **kwargs):
        super().__init__(**kwargs)
        self.browser = browser
        self.modal = True
        self.title = ft.Text(f"Браузер {self.browser.name}({self.browser.browser_id})")
        self.content = ft.Column([
            ft.Switch(
                label="Виключено" if not self.browser.active else "Включено",
                value=self.browser.active,
                width=50,
                height=50,
                on_change=self.change_model_status
            ),
            ft.TextField(
                value="\n".join([group_url.url for group_url in self.browser.twitter_group_urls]),
                multiline=True,
                min_lines=1,
                label="Список посилань на групи",
                hint_text="Кожне посилання з нового рядка",
                on_focus=self.clear_error_text,
                expand=True,
            ),
            ft.Row(
                [
                    ft.ElevatedButton("Скопіювати браузер id",
                                      on_click=lambda e: self.page.set_clipboard(self.browser.browser_id)),
                    ft.ElevatedButton("Скопіювати браузер name",
                                      on_click=lambda e: self.page.set_clipboard(self.browser.name)),
                    ft.ElevatedButton("Скопіювати браузер number",
                                      on_click=lambda e: self.page.set_clipboard(self.browser.serial_number)),
                ],
                wrap=True
            ),
        ],
            width=400,
            expand=True
        )
        self.expand = True
        self.actions = [
            ft.TextButton("Зберегти", on_click=self.save_links),
            ft.TextButton("Видалити", on_click=self.delete_browser, style=ft.ButtonStyle(color=ft.colors.RED)),
            ft.TextButton("Закрити", on_click=lambda e: self.page.close(self)),
        ]

    async def save_links(self, _: ft.ControlEvent):
        textfile: ft.TextField = self.content.controls[1]
        urls_list = textfile.value.strip().split("\n")
        filtered_urls = list(filter(None, urls_list))

        if filtered_urls:
            await TwitterGroupUrlController.create_batch([
                TwitterGroupUrl(url=group_url, browser_profile_id=self.browser.id)
                for group_url in filtered_urls
            ])
            self.page.close(self)
        else:
            textfile.error_text = "Поле не може бути порожнім"
            textfile.update()

    async def delete_browser(self, _: ft.ControlEvent):
        await BrowserProfileController.delete_browser_profile(self.browser.id)
        self.page.close(self)

    async def change_model_status(self, event: ft.ControlEvent):
        event.control.label = "Включено" if event.control.value else "Виключено"
        await BrowserProfileController.update_browser_profile_status(self.browser.id, event.control.value)
        event.control.update()

    async def clear_error_text(self, event: ft.ControlEvent):
        event.control.error_text = ""
        event.control.update()
