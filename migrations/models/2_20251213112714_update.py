from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "jokes" ADD "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "jokes" ADD "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "predictions" ADD "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "predictions" ADD "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "warnings" ADD "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "warnings" ADD "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "jokes" DROP COLUMN "updated_at";
        ALTER TABLE "jokes" DROP COLUMN "created_at";
        ALTER TABLE "warnings" DROP COLUMN "updated_at";
        ALTER TABLE "warnings" DROP COLUMN "created_at";
        ALTER TABLE "predictions" DROP COLUMN "updated_at";
        ALTER TABLE "predictions" DROP COLUMN "created_at";"""


MODELS_STATE = (
    "eJztmG1Po0AQx79K01eaeKbS1vbuXdWe1mhrlDuNxpAtbClX2MVlURvjd7+dBbpAEfVyOW"
    "uPd2Ue2JnfAP9Jn+oetbAbbB/TGQ7q32pPdYI8LH5kHVu1OvJ9ZQYDR2NXRv5ahIwDzpDJ"
    "hXGC3AALk4UDkzk+dygRVhK6LhipKQIdYitTSJy7EBuc2phPMROOm1thdoiFH2Vh8tKfGR"
    "MHu1amUMeCs6Xd4HNf2vYce0D4dxkLB44Nk7qhR1S8P+dTShYJDuFgtTHBDHEMJ3AWQgdQ"
    "YNxp0lRUrAqJqkzlWHiCQpenOn4jBpMSQCiqiYZhwylfvmpas9nRGs3dbrvV6bS7ja6IlS"
    "UtuzrPUcMKSHQriWVwOBjq0CgVc4qmB4ZnmYM4irIkbwWY40e+jFgX1mLASXwOsWgsjzgB"
    "WsY4MSjI6tn6O5RLgOn9K4nLC4I7FwzDn73z/aPe+cZp72pTeuax52Q0PEzCFd3h/sloT/"
    "JVPE2GoX8DFVA9EB7ueLiYbDYzx9eKU7eTH6tJuy56sEbEncevSxn9wWn/Qu+dnmVGcNDT"
    "++DRMvgT68buZnYCi5vULgf6UQ0ua9ejYV8SpAG3mTxRxenXdagJhZwahD4YyEq92Yk1AZ"
    "MZbOhbfzjYbGY12A8drCwe5GYyS30PwTBG5uwBMctY8lCNvhS77PI0L29BBNlyKsAWqozl"
    "94xhyzFhFIXqnHaXarSfC6yUulLqSqkrpf4vPuiVUq/pYFdJqS8RIwJ6oUwvfKUa/ZCOqg"
    "R6HQU6DDAz3ks5lfQ66hX5wvxD2oqu+KwFos53LEAqo1qBqhVojZWyWoHWdLCrtAL1MHPM"
    "adECFHtK1x+kYlZm+VmjzUfbaXVa3eZuayHBC0uZ8r6+09xjFjhFsrs/RayYXirls+iueO"
    "ofDRcTm8MDrrXbJcwS2RVRuc9Aosha5MtKLbwa74AYh39OgDuNxhsAiqgXAUpfblehhGNS"
    "oGfHF6PhC0uKSsmB/EFEgzfwp+lWzXUCfruaWEsoQtfl+2B+9cuJEdwA9sEPlZfn3wbWui"
    "s="
)
