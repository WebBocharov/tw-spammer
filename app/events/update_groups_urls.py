import flet as ft

from apis import ADSPowerLocalAPI
from database.controllers import BrowserProfileController
from spammer.spammer import TwitterSpammer


async def update_groups_urls_callback(event: ft.ControlEvent):
    # browser = await BrowserProfileController.get_browser_profile_by_id('kp73d9m')
    browsers = await BrowserProfileController.get_browser_profiles()

    for browser in browsers:
        browser_connection_data = await ADSPowerLocalAPI.open_browser(browser.browser_id)
        await TwitterSpammer.get_data_for_request(browser_connection_data, browser.browser_id)
