import asyncio
from dataclasses import asdict

from loguru import logger
from playwright.async_api import async_playwright, Error, Response

import config
from apis import ADSPowerLocalAPI
from apis.ads_power.dto import BrowserProfileConnectionDTO
from app.components import LogField
from database.controllers import ConfigController, TwitterGroupUrlController
from utils import get_random_gif
from .selectors import Selectors


class TwitterSpammer:
    def __init__(self, browser_id: str | None = None):
        self.browser_id = browser_id

    @logger.catch
    async def _init_playwright(self, browser_data: BrowserProfileConnectionDTO, *, slow_mo: int = 3000,
                               timeout: int = 60000):
        pl = await async_playwright().start()
        browser = await pl.chromium.connect_over_cdp(
            browser_data.ws_connection,
            slow_mo=slow_mo,
            timeout=timeout
        )
        default_context = browser.contexts[0]
        default_context.set_default_navigation_timeout(timeout)
        page = default_context.pages[0]
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return page, default_context

    @classmethod
    @logger.catch
    async def start(cls, browser_id: str, list_of_links: list[str], stop_event: asyncio.Event, log_field: LogField):
        spammer = cls()

        if stop_event.is_set():
            await log_field.write(f"{browser_id}: Парсінг зупинено")
            return

        browser_data = await ADSPowerLocalAPI.open_browser(browser_id)

        if not browser_data.active:
            await log_field.write(f"{browser_id}: Браузер не активний, не можу отримати дані від ADS Power")
            logger.error(f"Browser is not active, can't start spamming. Browser data: {asdict(browser_data)}")
            stop_event.set()
            return

        try:
            page, context = await spammer._init_playwright(browser_data)
        except Error as playwright_error:
            await log_field.write(f"{browser_id}: Помилка при створення парсера")
            logger.error(f"{browser_id}: Помилка при створення парсера - {playwright_error}")
            stop_event.set()
            return
        except Exception as error:
            await log_field.write(f"{browser_id}: Невідома помилка при створенні парсера")
            logger.error(f"{browser_id}: Невідома помилка при створенні парсера - {error}")
            stop_event.set()
            return

        while not stop_event.is_set():
            for group_url in list_of_links:
                if stop_event.is_set():
                    break

                gif_url = await get_random_gif()
                if gif_url is None:
                    logger.error("No gifs found")
                    await log_field.write(f"{browser_id}({group_url}): Помилка при отриманні gif")
                    stop_event.set()
                    return

                await log_field.write(f"{browser_id}({group_url}): Початок відправлення повідомлення")

                try:
                    await page.goto(group_url, wait_until="domcontentloaded")

                    if 'account/access' in page.url:
                        await log_field.write(f"{browser_id}({group_url}): Помилка доступу до сторінки. Captcha.")
                        logger.error(f"{browser_id}({group_url}): Access error. Captcha.")
                        stop_event.set()
                        return

                    await page.fill(Selectors.TEXT_FIELD, config.DEFAULT_TEXT)
                    await page.set_input_files(Selectors.FILE_INPUT, gif_url)
                    await page.click(Selectors.SUBMIT_BUTTON)
                    await log_field.write(f"{browser_id}({group_url}): Повідомлення відправлено")
                    logger.success(f"Message from {browser_id} sent to {group_url}")
                except Error as e:
                    await log_field.write(f"{browser_id}({group_url}): Помилка при парсінгу сторінки")
                    logger.error(f"{browser_id}({group_url}): Помилка при парсінгу сторінки - {e.message}")
                    continue

                if not stop_event.is_set():
                    await asyncio.sleep(int((await ConfigController.get_by_name("SPAM_TIMEOUT")).value) * 30)

        await log_field.write(f"{browser_id}: Парсінг зупинено")

    @classmethod
    async def get_page_source(cls, browser_data: BrowserProfileConnectionDTO):
        self = cls()
        page, _ = await self._init_playwright(browser_data)
        await page.goto("https://x.com/messages", wait_until="domcontentloaded")
        await page.wait_for_selector(Selectors.CHAT_LIST, state="visible", timeout=40000)
        await page.wait_for_timeout(5000)
        return await page.content()
