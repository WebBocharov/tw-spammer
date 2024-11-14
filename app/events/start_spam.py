import asyncio
from datetime import datetime

import flet as ft
from loguru import logger

from database.controllers import BrowserProfileController
from spammer.spammer import TwitterSpammer


async def start_spam_callback(_: ft.ControlEvent, browser_list, tasks, stop_events, log_field):
    browsers = await BrowserProfileController.get_browser_profiles_with_links()
    logger.info(f"Запуск спаму на {len(browsers)} браузерах")
    # Iterate over the profiles and access their TwitterGroupUrls
    for browser in browsers:
        urls = [group_url.url for group_url in browser.twitter_group_urls]
        log_field.update()
        if str(browser.id) not in tasks:
            stop_event = asyncio.Event()
            task = asyncio.create_task(TwitterSpammer.start(
                str(browser.browser_id),
                urls,
                stop_event,
                log_field
            ))
            await browser_list.update_status(f"{browser.id}")
            tasks[f"{browser.id}"] = task
            stop_events[f"{browser.id}"] = stop_event
