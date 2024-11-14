import flet as ft

from database.controllers import BrowserProfileController


async def filter_browser(event: ft.ControlEvent, filter_by_dropdown: ft.Dropdown):
    filter_by = next((option.key for option in filter_by_dropdown.options if option.key == filter_by_dropdown.value),
                     None) if filter_by_dropdown.value is not None else None
    query = event.data
    return await BrowserProfileController.filter_browser_profiles(filter_by, query)
