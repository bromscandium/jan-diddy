from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE SCHEMA IF NOT EXISTS "bot";
        CREATE SCHEMA IF NOT EXISTS "llm";
        ALTER TABLE "jokes" SET SCHEMA "bot";
        ALTER TABLE "predictions" SET SCHEMA "bot";
        ALTER TABLE "warnings" SET SCHEMA "bot";
        CREATE TABLE IF NOT EXISTS "llm"."messages" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "chat_id" BIGINT NOT NULL,
    "message_id" BIGINT NOT NULL,
    "thread_id" BIGINT,
    "user_id" BIGINT,
    "username" TEXT,
    "text" TEXT NOT NULL,
    "sent_at" TIMESTAMPTZ NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
        CREATE TABLE IF NOT EXISTS "llm"."bot_replies" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "chat_id" BIGINT NOT NULL,
    "message_id" BIGINT,
    "thread_id" BIGINT,
    "context" TEXT NOT NULL,
    "reply" TEXT NOT NULL,
    "success" BOOL,
    "reactions" INT NOT NULL DEFAULT 0,
    "scored_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
        CREATE TABLE IF NOT EXISTS "llm"."successful_dialogs" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "chat_id" BIGINT NOT NULL,
    "context" TEXT NOT NULL,
    "reply" TEXT NOT NULL,
    "score" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "llm"."bot_replies";
        DROP TABLE IF EXISTS "llm"."messages";
        DROP TABLE IF EXISTS "llm"."successful_dialogs";
        ALTER TABLE "bot"."jokes" SET SCHEMA "public";
        ALTER TABLE "bot"."predictions" SET SCHEMA "public";
        ALTER TABLE "bot"."warnings" SET SCHEMA "public";
        DROP SCHEMA IF EXISTS "llm";
        DROP SCHEMA IF EXISTS "bot";"""


MODELS_STATE = (
    "eJztWllz0zAQ/iuZPJWZwqTukcJb0gYI0ySdNhwDw3gUW3FEHcnYMm0H+t+R5Es+ISGljq"
    "M3Z4949Une/Xbtn+0lMaHtvegTegUdG0Gv/ar1s43BErKLAu1+qw0cJ9FxAQUzW5jPCNVd"
    "yXDmURcYlKnmwPYgE5nQM1zkUEQwk2LftrmQGMwQYSsR+Rh996FOiQXpArpM8eUrEyNswj"
    "sRo/jp3OhzBG0zFTMy+b2FXKf3jpD1kTXE9LWw5Tec6Qax/SVO7J17uiA4dkCYcqkFMXQB"
    "hfwO1PX5CniA4XqjRQXBJiZBlJKPCefAt6m04r+EwSCYQ8iiCfbF4nd5/lLTDg+7Wufw5P"
    "T4qNs9Pu2cMlsRUl7VfQgWnAAS/JWAZfhmOJ7yhRK2T8EecsGD8AEUBF4C7wRgYwGovirK"
    "ktOfoY6ArcI6EiRgJ2ds+9CWHjnoecCCKwOc9lsL4/C0Nh5iunAhMFdGOOWmAK4AmAVB4R"
    "3Nwztl0pL8kLhkoGXLqWd+qIBpOvgkQFp63nebC8Yfeldnb3tXe6Pep2dCcx9qLibjN5F5"
    "gun47GLSz6DKK+v9KpjGDgrRYkQ93zBY2ixIA4TYEOBiWCWvDLAz5lbLNFD1RE8mFylg+8"
    "Mscu9H/cHV3oFAmRkhWvLYs/Ro8MgKAC1Nqimf/8cMOv+cUrWDo+7R6eHJUZxJY0lVAs2j"
    "5hnEhaYOCtLlOVs1RUtYcg5lxwx0Zuj5IrrYtmM5HY4G19Pe6DJ1Ns970wHXaKkHPpLunT"
    "xLn9z4T1ofh9O3Lf6z9XkyHgjAiEctV9wxsZt+bvOYgE+JjsmtDkx52ZE4EqVrHjvJdK19"
    "THtuYCOfgitzajTBrNwE52hLdjY88rmN5c3l/EbqfrhgBoybW+Caek5DNFJmm1cttWVWAj"
    "Bj7mYILg8z7LvfkZvihjxQ7Ff14t9iE9WFN7ELX5VgK3ZdzQVV/m5Q/pY31nfMNTc27ak2"
    "9kk3VgRfk7o8CmZthaU51lVW56VspQp0Ewu0GpNvHu1ajMl3BmM1J39kgH0PuivDKzkpcP"
    "8ArrjOoVveJMk+azVK9ZqhPUafpPrODb+DgJiuM/xN3LazMdmSRkTNfnenxazV7PfShSYK"
    "X40VtJmyer+q03QyhqrZbGKzqaqymgarjK6mwbuysXWaBl8H3wPNffscAZtYhfU6b1RZtb"
    "3YXDcle1W8m1i81aR482irj1EflyCpj1E3jaj4nC+PaGkCiO138qtJRdAbweNqNXL5CFzM"
    "UC/kb7GukrbdylaKrDWRrD3JO7udIWssr3kszpV4ReShiIWaZTW+VKpZVuM2tk6zrB50kb"
    "EoIkChppL+gMSmNuSnQcznH5unck7zA7oeKiq7ZwvgFqMnuWxL3WWn/k63IbYoP+Da8XEF"
    "ZlHZZVaZNBBVZC3QpUstfzRWADE0304ADzqdvwCQWZUCKHQFwzpcUM/eXU/GFcM6XFjIkE"
    "Fbv1o28mrKsSvw4+utZoJZ0pcpQ/wPOBN80sLy8BszTzks"
)
