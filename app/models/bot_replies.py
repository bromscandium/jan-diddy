from tortoise import fields
from tortoise.models import Model


class BotReplies(Model):
    id = fields.BigIntField(primary_key=True)
    chat_id = fields.BigIntField()
    message_id = fields.BigIntField(null=True)
    thread_id = fields.BigIntField(null=True)
    context = fields.TextField()
    reply = fields.TextField()
    success = fields.BooleanField(null=True)
    reactions = fields.IntField(default=0)
    scored_at = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        schema = "llm"
        table = "bot_replies"
