import asyncio

import flet as ft
from bs4 import BeautifulSoup
from loguru import logger

from apis import ADSPowerLocalAPI
from database.controllers import BrowserProfileController, TwitterGroupUrlController
from spammer import TwitterSpammer

@logger.catch
async def update_groups_urls_callback(event: ft.ControlEvent):
    browsers = await BrowserProfileController.get_browser_profiles()

    for browser in browsers:
        browser_connection_data = await ADSPowerLocalAPI.open_browser(browser.browser_id)
        logger.info(f"Getting groups urls for browser: {browser.browser_id}")
        asyncio.create_task(parse_groups(browser_connection_data, browser.browser_id))


@logger.catch
async def parse_groups(browser_connection, browser_id):
    logger.info(f"Getting page source for browser {browser_id}")
    page_source = await TwitterSpammer.get_page_source(browser_connection)
    logger.info(f"Got page source for browser {browser_id}")

    bs4 = BeautifulSoup(page_source, 'html.parser')
    bs4_conv = bs4.find('main', {'role': 'main'}).find('div', {'role': 'tablist'}).find_all(recursive=False)
    conversation_urls = []

    for conversation in bs4_conv:
        conv_url = conversation.find_next(
            'a',
            {'data-testid': 'DM_Conversation_Avatar', 'role': 'link'}
        ).get('href')
        logger.info(f"Getting conversation url {conv_url}")

        if conv_url is not None:
            conversation_urls.append(f"https://x.com/messages/{conv_url.split('/')[2]}")
        else:
            logger.info(f"Conversation url is None - {conv_url}")

    await TwitterGroupUrlController.batch_create_by_browser_id(
        set(conversation_urls),
        browser_id
    )

    logger.info(f"Added {len(set(conversation_urls))} urls to database")
