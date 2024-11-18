from database.models import Config


class ConfigController:
    @staticmethod
    async def create(name: str, value):
        if not await Config.exists(name=name):
            await Config.create(name=name, value=value)

    @staticmethod
    async def create_or_update(name: str, value):
        if await Config.exists(name=name):
            await Config.filter(name=name).update(value=value)
        else:
            await Config.create(name=name, value=value)

    @staticmethod
    async def get_by_name(name: str):
        return await Config.filter(name=name).first()
