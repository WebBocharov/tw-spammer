import uuid

from tortoise import fields
from tortoise.models import Model


class BaseModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True


class BrowserProfile(BaseModel):
    name = fields.CharField(max_length=50)
    browser_id = fields.CharField(max_length=50)
    active = fields.BooleanField(default=False)
    serial_number = fields.CharField(max_length=50, null=True)

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
