from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "jokes" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "text" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "predictions" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "text" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "warnings" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "user_id" BIGINT NOT NULL,
    "warnings" INT NOT NULL,
    "reason" TEXT NOT NULL
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
    "eJztl29v2jAQxr8K4tUqdRMNUNjeUbR1VB1MHdsqVVVkEhM8Eju1nRVU8d3nc/44hJAVbd"
    "qg4h08dxff/eKHE0/1gLnYF2+u2ByL+rvaU52iAKsP64HTWh2FoZFBkGji68wfWcpESI4c"
    "qcQp8gVWkouFw0koCaNKpZHvg8gclUioZ6SIkocI25J5WM4wV4G7eyUT6uKFbkx/Def2lG"
    "DfXWuUuHC21m25DLV2QbwBlR90Lhw4sR3mRwE1+eFSzhjNCgiVoHqYYo4khhMkj2ACaDCZ"
    "NB0qbtakxF3malw8RZEvcxM/E4PDKCBU3cQvw4NTXr+1rGazYzWa5912q9Npdxtdlatb2g"
    "x1VvHABkj8KI1lcDkYjmFQpt5T/PZAWOkaJFFcpXkbwBIv5CbisVLLAaf5BcRqsCLiFGgV"
    "41QwkM3d+juUK4CN399qXIEQDz4Iw2+9m/7H3s2rT73bEx1ZJpHr0fAyTTd0h/3r0YXiC7"
    "d3Os/hBWGCnPkj4q69EWEW25a7GQqsoKggijzNCiaG+RI3f+bYJQ4AKjV7Plxp+bCQeDT+"
    "0fhH4++x8b8jThWKUtdnsUrLP+azjn5/iX6PBOb2rpRzRb9HvR++/5e0Dd28gdbxbmWbLz"
    "kwuNZZq9PqNs9bGdNMqUK5iY1jJFQHO6whU3FcRHu3iHqYE2dWtoaSSOUSQiZnb1bQC9o/"
    "f2ja7ZvlJ+aClLm4P0O8nF6u5FBsrG79wvYx9SRccKvdrmCWulhlnRQMm4SsOLb+awjW2A"
    "Fikn6YAM8ajWcAVFlbAerYOkB1osS05G/N1ZfRsBxirqQA8itVA97BP+HTmk+EvN9PrBUU"
    "Yerq9VLcJECBCelx/RT9gP++Xla/AOLckLs="
)
