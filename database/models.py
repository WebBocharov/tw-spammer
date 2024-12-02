import re
import uuid

from tortoise import fields
from tortoise.models import Model
from tweety import constants
from tweety.types import Proxy

import config


class BaseModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True


class BrowserProfile(BaseModel):
    name = fields.CharField(max_length=50)
    browser_id = fields.CharField(max_length=50)
    active = fields.BooleanField(default=False)
    serial_number = fields.CharField(max_length=50, null=True)
    proxy = fields.CharField(max_length=225, null=True)

    @property
    def proxy_obj(self) -> Proxy | None:
        if not self.proxy:
            return None

        proxy_regex = re.compile(config.PROXY_REGEX).match(self.proxy)

        return Proxy(
            proxy_type=constants.HTTP,
            host=proxy_regex.group(2),
            port=proxy_regex.group(3),
            username=proxy_regex.group(4),
            password=proxy_regex.group(5)
        )

    class Meta:
        app = "models"


class TwitterGroupUrl(BaseModel):
    url = fields.TextField()
    browser_profile = fields.ForeignKeyField(
        "models.BrowserProfile",
        related_name="twitter_group_urls",
        null=False
    )

    class Meta:
        app = "models"


class Config(BaseModel):
    name = fields.CharField(max_length=50)
    value = fields.TextField()

    class Meta:
        app = "models"
