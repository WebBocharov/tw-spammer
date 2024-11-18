import asyncio

import flet as ft
from loguru import logger

from database.controllers import ConfigController


class SetSpamTimeoutModal(ft.AlertDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modal = True
        self.title = ft.Text(f"Встановлення таймауту спаму")
        self.content = ft.TextField(
            value=asyncio.run(ConfigController.get_by_name("SPAM_TIMEOUT")).value,
            label="Введіть таймаут",
            hint_text="1 = 30 секунд",
            expand=True,
            prefix=ft.Text("30 секунд * "),
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.expand = True
        self.actions = [
            ft.TextButton("Зберегти", on_click=self.save_timeout),
            ft.TextButton("Закрити", on_click=lambda e: self.page.close(self)),
        ]

    async def save_timeout(self, _: ft.ControlEvent):
        if int(self.content.value) > 0:
            await ConfigController.create_or_update("SPAM_TIMEOUT", int(self.content.value))
            logger.info(f"Timeout set to {(await ConfigController.get_by_name("SPAM_TIMEOUT")).value} minutes")
            self.page.close(self)
