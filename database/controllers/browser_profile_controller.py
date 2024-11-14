from dataclasses import asdict

from tortoise.functions import Count

from apis.ads_power.dto import BrowserProfileInfoDTO
from database.models import BrowserProfile


class BrowserProfileController:
    @staticmethod
    async def create_browser_profile(browser: BrowserProfileInfoDTO):
        return await BrowserProfile.get_or_create(**asdict(browser))

    @staticmethod
    async def delete_browser_profile_by_filer(filter_by: str, value: list[str]):
        await BrowserProfile.filter(**{filter_by: value}).delete()

    @staticmethod
    async def batch_create(browsers: list[BrowserProfileInfoDTO]):
        for browser in browsers:
            await BrowserProfile.get_or_create(**asdict(browser))

    @staticmethod
    async def delete_browser_profile(browser_id: str):
        await BrowserProfile.filter(browser_id=browser_id).delete()

    @staticmethod
    async def get_browser_profiles() -> list[BrowserProfile]:
        return await BrowserProfile.all().prefetch_related('twitter_group_urls')

    @staticmethod
    async def filter_browser_profiles(field_filter_by: str, value: str) -> list[BrowserProfile]:
        return await BrowserProfile.filter(**{f"{field_filter_by}__icontains": value}).all().prefetch_related('twitter_group_urls')

    @staticmethod
    async def get_browser_profiles_with_links() -> list[BrowserProfile]:
        return await BrowserProfile.annotate(
            url_count=Count('twitter_group_urls')
        ).filter(url_count__gt=0, active=True).prefetch_related('twitter_group_urls')

    @staticmethod
    async def update_browser_profile_status(browser_id: str, status: bool):
        return await BrowserProfile.filter(id=browser_id).update(active=status)