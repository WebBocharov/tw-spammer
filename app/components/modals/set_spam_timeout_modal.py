import flet as ft
from loguru import logger

import config


class SetSpamTimeoutModal(ft.AlertDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modal = True
        self.title = ft.Text(f"Встановлення таймауту спаму")
        self.content = ft.TextField(
            value=config.SPAM_TIMEOUT,
            label="Введіть таймаут",
            hint_text="1 = 30 секунд",
            expand=True,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.expand = True
        self.actions = [
            ft.TextButton("Зберегти", on_click=self.save_timeout),
            ft.TextButton("Закрити", on_click=lambda e: self.page.close(self)),
        ]

    async def save_timeout(self, _: ft.ControlEvent):
        if int(self.content.value) > 0:
            config.SPAM_TIMEOUT = int(self.content.value)
            logger.info(f"Timeout set to {config.SPAM_TIMEOUT} minutes")
            self.page.close(self)
