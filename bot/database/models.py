from tortoise import fields
from tortoise.models import Model


class User(Model):
    user_id = fields.BigIntField(pk=True)
