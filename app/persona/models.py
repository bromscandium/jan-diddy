from tortoise import fields
from tortoise.models import Model


class LLMModel(Model):
    id = fields.BigIntField(primary_key=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True
        schema = "llm"


class Messages(LLMModel):
    chat_id = fields.BigIntField()
    message_id = fields.BigIntField()
    thread_id = fields.BigIntField(null=True)
    user_id = fields.BigIntField(null=True)
    username = fields.TextField(null=True)
    text = fields.TextField()
    sent_at = fields.DatetimeField()

    class Meta(LLMModel.Meta):
        abstract = False
        table = "messages"


class BotReplies(LLMModel):
    chat_id = fields.BigIntField()
    message_id = fields.BigIntField(null=True)
    thread_id = fields.BigIntField(null=True)
    context = fields.TextField()
    reply = fields.TextField()
    success = fields.BooleanField(null=True)
    reactions = fields.IntField(default=0)
    scored_at = fields.DatetimeField(null=True)

    class Meta(LLMModel.Meta):
        abstract = False
        table = "bot_replies"


class SuccessfulDialogs(LLMModel):
    chat_id = fields.BigIntField()
    context = fields.TextField()
    reply = fields.TextField()
    score = fields.IntField(default=0)

    class Meta(LLMModel.Meta):
        abstract = False
        table = "successful_dialogs"


class UserProfiles(LLMModel):
    user_id = fields.BigIntField(unique=True, db_index=True)
    username = fields.TextField(null=True)
    engagement_score = fields.IntField(default=0)
    replies_to_them = fields.IntField(default=0)
    successes = fields.IntField(default=0)
    last_seen = fields.DatetimeField(null=True)

    class Meta(LLMModel.Meta):
        abstract = False
        table = "user_profiles"
