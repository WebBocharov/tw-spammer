import asyncio

import flet as ft
from flet_core.types import AppView
from loguru import logger

from apis import ADSPowerLocalAPI
from app.components import BrowsersListView, LogField, SearchField
from app.components.buttons import StartSpamButton, StopSpamButton
from app.components.modals import SetSpamTimeoutModal
from app.events import start_spam_callback, stop_spam_callback, update_groups_urls_callback
from database.controllers import BrowserProfileController, ConfigController

from database.init import init_orm
from app.events.filter import filter_browser

logger.add(
    "logs/{time:%d.%m.%Y}.log",
    rotation="1 day",
    retention="1 week",
    compression="zip",
    diagnose=True,
    enqueue=True,
    backtrace=True,
)


async def main(page: ft.Page):
    page.title = "Twitter Spammer"
    page.theme_mode = ft.ThemeMode.DARK

    await init_orm()
    await ConfigController.create("SPAM_TIMEOUT", 2)  # 1 minute
    browsers_list_view = BrowsersListView()
    await browsers_list_view.set_controls(await BrowserProfileController.get_browser_profiles())

    async def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "S" and e.ctrl:
            page.show_semantics_debugger = not page.show_semantics_debugger
            page.update()

    page.on_keyboard_event = on_keyboard

    tasks = {}
    stop_events = {}

    async def update_browser_list(_: ft.ControlEvent):
        updated_browser_list = await ADSPowerLocalAPI.get_browsers()

        if updated_browser_list:
            await BrowserProfileController.batch_create(updated_browser_list)
            await BrowserProfileController.delete_browser_profile_by_filer("browser_id__not_in",
                                                                           [browser.browser_id for browser in
                                                                            updated_browser_list])

        list_view = await browsers_list_view.set_controls(await BrowserProfileController.get_browser_profiles())
        list_view.update()

    page.appbar = ft.AppBar(
        title=ft.Text("Twitter Spammer"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.PopupMenuButton(items=[
                ft.PopupMenuItem(text="Установити timeout спаму", on_click=lambda _: page.open(SetSpamTimeoutModal())),
                ft.PopupMenuItem(text="Обновити список посилань на групи", on_click=update_groups_urls_callback),
                ft.PopupMenuItem(text="Оновити список браузерів", on_click=update_browser_list),
            ]),
        ],
    )

    filter_by_dropdown = ft.Dropdown(
        value="name",
        label="Filter",
        width=220,
        border_color=ft.colors.WHITE,
        options=[
            ft.dropdown.Option("name", "By name"),
            ft.dropdown.Option("browser_id", "By browser id")
        ]
    )
    search_field = SearchField(
        lambda e: filter_browser(
            e,
            filter_by_dropdown
        ),
        browsers_list_view,
        label="Search",
        width=220,
        border_color=ft.colors.WHITE
    )
    logs_text_field = LogField()

    page.add(
        ft.Container(
            alignment=ft.alignment.top_center,
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Row([search_field, filter_by_dropdown]),
                            browsers_list_view,
                        ]
                    ),
                    ft.Column(
                        controls=[logs_text_field],
                        expand=True,
                    ),
                ],
            ),
            expand=True,
        ),
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    content=StartSpamButton(
                                        lambda _: start_spam_callback(
                                            _,
                                            browsers_list_view,
                                            tasks,
                                            stop_events,
                                            logs_text_field
                                        ),
                                    ),
                                    alignment=ft.alignment.center,
                                ),
                                ft.Container(
                                    content=StopSpamButton(
                                        lambda _: stop_spam_callback(
                                            _,
                                            browsers_list_view,
                                            tasks,
                                            stop_events
                                        )
                                    ),
                                    alignment=ft.alignment.center,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        alignment=ft.alignment.bottom_center,
                    )
                ]
            )
        )
    )


if __name__ == '__main__':
    asyncio.run(ft.app_async(main, view=AppView.FLET_APP))
