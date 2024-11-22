from loguru import logger

from database.controllers import BrowserProfileController
from database.models import TwitterGroupUrl


class TwitterGroupUrlController:
    @staticmethod
    async def create_batch(twitter_group_urls: list[TwitterGroupUrl]):
        for twitter_group_url in twitter_group_urls:
            await TwitterGroupUrl.get_or_create(
                url=twitter_group_url.url,
                browser_profile_id=getattr(twitter_group_url, "browser_profile_id")
            )

    @staticmethod
    @logger.catch
    async def batch_create_by_browser_id(group_urls: list[str] | set[str], browser_id):
        browser_profile = await BrowserProfileController.get_browser_profile_by_id(browser_id)
        await TwitterGroupUrl.filter(browser_profile=browser_profile).delete()
        for group_url in group_urls:
            await TwitterGroupUrl.get_or_create(
                url=group_url,
                browser_profile=browser_profile
            )
