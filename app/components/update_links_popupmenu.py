import asyncio

import flet as ft
from loguru import logger
from tweety import TwitterAsync

import config
from apis import ADSPowerLocalAPI
from app.components import LogField
from database.controllers import BrowserProfileController, TwitterGroupUrlController
from spammer import TwitterSpammer


class UpdateLinksPopUpMenu(ft.PopupMenuItem):
    def __init__(self, logging_field: LogField, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = "Обновити список посилань на групи"
        self.on_click = self.click_callback
        self.logging_field = logging_field

    @logger.catch
    async def click_callback(self, _: ft.ControlEvent):
        logger.info("Updating groups urls")
        browsers = await BrowserProfileController.get_browser_profiles()

        for browser in browsers:
            browser_connection_data = await ADSPowerLocalAPI.open_browser(browser.browser_id)
            logger.info(f"Getting groups urls for browser: {browser.browser_id}")
            await self.logging_field.write(f"Отримання посилань на групи для браузера {browser.browser_id}")
            asyncio.create_task(self.parse_groups(browser_connection_data, browser.browser_id))

    @logger.catch
    async def parse_groups(self, browser_connection, browser_id):
        logger.info(f"Getting page source for browser {browser_id}")
        cookies = await TwitterSpammer.get_cookies(browser_connection)
        browser = await BrowserProfileController.get_browser_profile_by_id(browser_id)

        app = TwitterAsync(
            f"{config.SESSIONS_FOLDER}/{browser_id}",
            proxy=browser.proxy_obj if browser.proxy else None,
        )
        await app.load_cookies(cookies)

        conversations = [
            f"https://x.com/messages/{group.id}"
            for group in await app.get_inbox(pages=100) if len(group.participants) >= 50 and group.trusted
        ]
        await TwitterGroupUrlController.batch_create_by_browser_id(conversations, browser_id)
        await self.logging_field.write(f"Отримано {len(conversations)} груп для браузера {browser_id}")

        logger.info(f"Got {len(conversations)} conversations for browser {browser_id}")
        logger.info(f"Groups urls for browser {browser_id} updated")
