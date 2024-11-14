from database.models import TwitterGroupUrl


class TwitterGroupUrlController:
    @staticmethod
    async def create_batch(twitter_group_urls: list[TwitterGroupUrl]):
        for twitter_group_url in twitter_group_urls:
            await TwitterGroupUrl.get_or_create(
                url=twitter_group_url.url,
                browser_profile_id=getattr(twitter_group_url, "browser_profile_id")
            )