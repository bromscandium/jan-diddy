from tortoise import fields
from tortoise.models import Model


class Warnings(Model):
    id = fields.BigIntField(primary_key=True)
    user_id = fields.BigIntField()
    reason = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)