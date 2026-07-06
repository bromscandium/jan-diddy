from tortoise import fields
from tortoise.models import Model


class Predictions(Model):
    id = fields.BigIntField(primary_key=True)
    text = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        schema = "bot"
        table = "predictions"
