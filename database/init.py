from tortoise import Tortoise

TORTOISE_ORM = {
    "connections": {"default": "sqlite://main.db"},
    "apps": {
        "models": {
            "models": ["database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_orm():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()