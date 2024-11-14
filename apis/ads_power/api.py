import asyncio

import aiohttp
from loguru import logger

from .dto import BrowserProfileConnectionDTO, BrowserProfileInfoDTO
import config


class ADSPowerLocalAPI:
    API_URL = config.ADS_POWER_API_URL

    @classmethod
    async def get_browsers(cls):
        logger.info(f"Getting browsers from ADS Power")
        browsers_profiles = []
        async with aiohttp.ClientSession() as session:
            page = 1
            while True:
                async with session.get(f"{cls.API_URL}/api/v1/user/list?page_size=100&page={page}") as response:
                    logger.info(f"Response status: {response.status}, page: {page}, response: {await response.text()}")
                    if response.status == 200 and (await response.json()).get("code", -1) == 0 and (
                    await response.json()).get("data", {}).get("list", []) != []:
                        browsers_profiles.extend([
                            BrowserProfileInfoDTO(
                                name=browser.get("name"),
                                browser_id=browser.get("user_id"),
                                serial_number=browser.get("serial_number")
                            ) for browser in (await response.json()).get("data", {}).get("list", [])])
                        page += 1
                        await asyncio.sleep(1.2)
                    else:
                        break
            return browsers_profiles

    @classmethod
    async def browser_status(cls, browser_id: str):
        logger.info(f"Getting browser status for {browser_id}")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{cls.API_URL}/api/v1/browser/active?user_id={browser_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("code") == 0:
                        browser_status = data.get("data", {}).get("status", "Inactive").lower()
                        return BrowserProfileConnectionDTO(
                            active=True if browser_status == "active" else False,
                            ws_connection=data.get("data", {}).get("ws", {}).get("puppeteer", ""),
                            full_object=data
                        )
                    else:
                        logger.error(f"Error while getting browser status: {data}")
                        return BrowserProfileConnectionDTO(active=False, ws_connection="", full_object=data)
                else:
                    logger.error(f"Error while getting browser status: {response.content}")
                    return BrowserProfileConnectionDTO(active=False, ws_connection="", full_object=response.content)

    @classmethod
    async def open_browser(cls, browser_id: str) -> BrowserProfileConnectionDTO:
        logger.info(f"Trying to open browser {browser_id}")
        browser_status = await cls.browser_status(browser_id)
        if browser_status.active:
            logger.info(f"Browser {browser_id} is already active")
            return browser_status
        else:
            logger.info(f"Browser {browser_id} is inactive. Starting...")
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{cls.API_URL}/api/v1/browser/start?user_id={browser_id}&headless=1") as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("code") == 0:
                            return BrowserProfileConnectionDTO(
                                active=True,
                                ws_connection=data.get("data", {}).get("ws", {}).get("puppeteer", ""),
                                full_object=data
                            )
                        else:
                            logger.error(f"Error while starting browser: {data}")
                            return BrowserProfileConnectionDTO(active=False, ws_connection="", full_object=data)
                    else:
                        logger.error(f"Error while starting browser: {response.content}")
                        return BrowserProfileConnectionDTO(active=False, ws_connection="", full_object=response.content)
