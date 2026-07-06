from tortoise import fields
from tortoise.models import Model


class Messages(Model):
    id = fields.BigIntField(primary_key=True)
    chat_id = fields.BigIntField()
    message_id = fields.BigIntField()
    thread_id = fields.BigIntField(null=True)
    user_id = fields.BigIntField(null=True)
    username = fields.TextField(null=True)
    text = fields.TextField()
    sent_at = fields.DatetimeField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        schema = "llm"
        table = "messages"
