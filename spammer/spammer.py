import asyncio
from dataclasses import asdict

from loguru import logger
from playwright.async_api import async_playwright, Error

import config
from apis import ADSPowerLocalAPI
from app.components import LogField
from utils import get_random_gif
from .selectors import Selectors


class TwitterSpammer:
    __slots__ = ("browser_id", "list_of_links", "stop_event", "log_field")

    def __init__(self, browser_id: str, list_of_links: list[str], *, stop_event: asyncio.Event,
                 log_field: LogField):
        self.browser_id = browser_id
        self.list_of_links = list_of_links
        self.stop_event = stop_event
        self.log_field = log_field

    @classmethod
    @logger.catch
    async def start(cls, browser_id: str, list_of_links: list[str], stop_event: asyncio.Event, log_field: LogField):
        if stop_event.is_set():
            await log_field.write(f"Парсінг в браузері {browser_id} зупинено")
            return

        spammer = cls(
            browser_id,
            list_of_links,
            stop_event=stop_event,
            log_field=log_field
        )

        browser_data = await ADSPowerLocalAPI.open_browser(browser_id)

        logger.info(asdict(browser_data))

        if not browser_data.active:
            await log_field.write(f"Помилка при відкритті браузера {browser_id}")
            logger.error(f"Browser is not active, can't start spamming. Browser data: {asdict(browser_data)}")
            spammer.stop_event.set()
            return

        try:
            pl = await async_playwright().start()
            browser = await pl.chromium.connect_over_cdp(
                browser_data.ws_connection,
                slow_mo=3000,
                timeout=60000
            )
            default_context = browser.contexts[0]
            default_context.set_default_navigation_timeout(60000)
            page = default_context.pages[0]
            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Error as playwright_error:
            await log_field.write(f"{browser_id}: Помилка при створення парсера")
            logger.error(f"{browser_id}: Помилка при створення парсера - {playwright_error}")
            spammer.stop_event.set()
            return
        except Exception as error:
            await log_field.write(f"{browser_id}: Невідома помилка при створенні парсера")
            logger.error(f"{browser_id}: Невідома помилка при створенні парсера - {error}")
            spammer.stop_event.set()
            return

        while not spammer.stop_event.is_set():
            for group_url in spammer.list_of_links:
                if spammer.stop_event.is_set():
                    break

                gif_url = await get_random_gif()
                if gif_url is None:
                    logger.error("No gifs found")
                    await log_field.write(f"Не знайдено файлів в папці з медіа ({browser_id})")
                    spammer.stop_event.set()
                    return

                await log_field.write(f"Відбувається відправка в {browser_id} браузері в групу {group_url}")

                try:
                    await page.goto(group_url, wait_until="domcontentloaded")
                    await page.mouse.dblclick(60, 60, delay=700)
                    await page.wait_for_selector(Selectors.TEXT_FIELD)
                    await page.set_input_files(Selectors.FILE_INPUT, gif_url)
                    await page.click(Selectors.SUBMIT_BUTTON)
                    logger.info(f"Message sent to {group_url}")
                except Error as e:
                    await log_field.write(f"{browser_id}({group_url}): Помилка при парсінгу сторінки")
                    logger.error(f"{browser_id}({group_url}): Помилка при парсінгу сторінки - {e}")
                    continue

                if not spammer.stop_event.is_set():
                    await asyncio.sleep(config.SPAM_TIMEOUT * 30)

        await log_field.write(f"Парсінг в браузері {browser_id} зупинено")
