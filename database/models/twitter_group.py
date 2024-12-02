from tortoise import fields

from .base import BaseModel


class TwitterGroupUrl(BaseModel):
    url = fields.TextField()
    browser_profile = fields.ForeignKeyField(
        "models.BrowserProfile",
        related_name="twitter_group_urls",
        null=False
    )

    class Meta:
        app = "models"
