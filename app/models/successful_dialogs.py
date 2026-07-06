from tortoise import fields
from tortoise.models import Model


class SuccessfulDialogs(Model):
    id = fields.BigIntField(primary_key=True)
    chat_id = fields.BigIntField()
    context = fields.TextField()
    reply = fields.TextField()
    score = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        schema = "llm"
        table = "successful_dialogs"
