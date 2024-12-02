import uuid

from tortoise import fields, Model


class BaseModel(Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True
