from tortoise import fields

from .base import BaseModel


class Config(BaseModel):
    name = fields.CharField(max_length=50)
    value = fields.TextField()

    class Meta:
        app = "models"
