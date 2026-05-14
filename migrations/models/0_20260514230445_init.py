from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "jokes" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "text" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "predictions" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "text" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "warnings" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "user_id" BIGINT NOT NULL,
    "reason" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztlm1P2zAQx79K1FcgbaikLe32rkAHRdAiiAZimiI3cVOviR0SZ1Axvvt8TlInaQgwTa"
    "N0edfeQ3z3u8T/e2h4zMZuuHPC5jhsfNYeGhR5WPzIOz5oDeT7ygwGjiaujPyxDJmEPEAW"
    "F8YpckMsTDYOrYD4nDAqrDRyXTAySwQS6ihTRMlthE3OHMxnOBCOb9+FmVAb38vC5F9/bk"
    "4Jdu1cocSGs6Xd5Atf2vaJM6T8i4yFAyemxdzIoyreX/AZo8sEQjlYHUxxgDiGE3gQQQdQ"
    "YNJp2lRcrAqJq8zk2HiKIpdnOn4hBotRQCiqiYfhwCkfP+l6q9XVm629Xqfd7XZ6zZ6IlS"
    "WturqPccMKSPwoiWV4NBwZ0CgTc4qnB4ZHmYM4irMkbwWY43u+itgQ1nLAaXwBsWisiDgF"
    "WsU4NSjI6t36O5QrgBmDa4nLC8NbFwyjr/2Lg+P+xdZZ/3pbehaJ53Q8OkrDFd3Rwel4X/"
    "JVPK0AQ/8mKqF6KDyceLicbD6zwNdOUnfSH+tJuyF6sMfUXSSfSxX94dng0uifnedGcNg3"
    "BuDRc/hT69bedn4Cy4doV0PjWIO/2s14NJAEWcidQJ6o4oybBtSEIs5Myu5MZGe+7NSags"
    "kNNvLtPxxsPrMe7JsOVhYPcjOdZ+5DMEyQNb9DgW2ueJjOnopddXm6V7Qgihw5FWALVSby"
    "ex5gm1gwilJ1zrorNdovBNZKXSt1rdS1Uv8XF3qt1Bs62HVS6isUUAG9VKaXvkqNvstG1Q"
    "K9iQIdhTgwX0s5k/Q86jW5Yf4hbUVXXGuhqPMVC5DKqFegegXaYKWsV6ANHew6rUB9HBBr"
    "VrYAJZ7K9QepmLVZfjZo89F32912r7XXXkrw0lKlvM/vND9xEJIy2T2YoaCcXiblveiueO"
    "vvTRdTh8MLrnc6FcxS2RVRhWsgVWQ99uWlFj6NV0BMwt8nwN1m8wUARdSTAKWvsKswyjEt"
    "0bOTy/HoiSVFpRSFjFhc+6W5JFzTHbuCH/RbvQkWl76CDMEDYBN8U2F5/A0VpLfa"
)
