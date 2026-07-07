from tortoise import fields
from tortoise.models import Model


class BotModel(Model):
    id = fields.BigIntField(primary_key=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
        schema = "bot"


class Jokes(BotModel):
    text = fields.TextField()

    class Meta(BotModel.Meta):
        abstract = False
        table = "jokes"


class Predictions(BotModel):
    text = fields.TextField()

    class Meta(BotModel.Meta):
        abstract = False
        table = "predictions"


class Warnings(BotModel):
    user_id = fields.BigIntField()
    reason = fields.TextField()

    class Meta(BotModel.Meta):
        abstract = False
        table = "warnings"
