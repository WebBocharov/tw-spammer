from loguru import logger

from app.components import BrowsersListView


async def stop_spam_callback(_, browser_list: BrowsersListView, tasks: dict, stop_events: dict):
    for i in list(tasks.keys()):
        logger.info(f"Зупинка функції, id: {i}")
        stop_events[i].set()
        await browser_list.update_status(i)
        del tasks[i]
        del stop_events[i]
