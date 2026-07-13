from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "llm"."successful_dialogs" ADD COLUMN IF NOT EXISTS "verdict" TEXT;
        ALTER TABLE "llm"."successful_dialogs" ADD COLUMN IF NOT EXISTS "mood" TEXT;
        ALTER TABLE "llm"."successful_dialogs" ADD COLUMN IF NOT EXISTS "mode" TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "llm"."successful_dialogs" DROP COLUMN IF EXISTS "verdict";
        ALTER TABLE "llm"."successful_dialogs" DROP COLUMN IF EXISTS "mood";
        ALTER TABLE "llm"."successful_dialogs" DROP COLUMN IF EXISTS "mode";"""


MODELS_STATE = (
    "eJztW1tz2jgU/isMT+kM2yHkuvsGKdvSCZBJ6LbTnR2PsIXxxpZcW27CdPPfV5LvRnZq2h"
    "QD582cC5a+Y51zPsn+1naogW3/9YCyW+zaFvbbf7S+tQlyML9QaDutNnLdVCcEDM1taT6n"
    "TPMyhnOfeUhnXLVAto+5yMC+7lkusyjhUhLYthBSnRtaxExFAbG+BFhj1MRsiT2u+PsfLr"
    "aIgR/lGOVP915bWNg2cmO2DHFvKdfYypWygWWOCPtT2oobzjWd2oFDUnt3xZaUJA4WYUJq"
    "YoI9xLC4A/MCMQMxwGi+8aTCwaYm4SgzPgZeoMBmmRl/Jww6JQJCPpowLqa4y2+/93onJx"
    "e97sn55dnpxcXZZfeS28ohrasunsIJp4CEfyVhGb0dTWZiopTHKYyhEDxJH8RQ6CXxTgHW"
    "PSwg0RBbB/oN1zDLwWqo854FyI3I9XV8UQxADHdVBGJBGoL0yftJMeBzMKbEXkXhrYB3Nh"
    "oP72b98Y2YieP7X2wJUX82FJqelK4K0qPzV/l4JH/S+jiavWuJn63P08lQIkh9Znryjqnd"
    "7HNbjAkFjGqEPmjIyDyJsTQGhltmArtETKu7fDJOz6+hhoTwFy6jTC7Fvo9MXBvgvN9GGE"
    "fB33uI2VIsztoI59wA4AqA+SAYflTk/RmXluSH1KUALZ9OM/NDVUoffprlsvnkr/7t1bv+"
    "7dG4/+lVLqNfTydvY/MU08nV9XRQQFW0TKs6mCYOgKgaUT/QdZ42FWmAUhsjooY141UAds"
    "7dGpkGqlb0dHqdA3YwKiL3YTwY3h4dS5S5kcVKlj1Pj7oYmQLQ0qSa8/l1nUH3h1Nq7/j0"
    "4vTy5Pw0yaSJpCqBrqPm69TbqE3OOf6ELrlRj2WTmuJ42mtdsSCXi/sM+xGCOdLvH5BnaG"
    "sa2qNltusqp+cUJYjwBs+I0BTjjHj3OGz9lJw80XWqGLmTtQI6DnQc6HgjMg/Q8W1TmS3S"
    "8YPBGPj4CwMc+NirDW/GCcB9Blx5vYZuOTPP+mxEzpvVq78EN6+7gQS7R8/sdWDCNiGZqd"
    "tudn470uk1nWPehZtei8B+YyGbmkqyuW7UqWKdfmKuGRl74J/AP4F/NiIrAf/cdncJ3Ai4"
    "0e6Cy6hr6bW6+NgBWJGyi4eTdThZ3wVE5dlkjWPgxP4gj4C/Ys+w9FqrOuMCqVL5CDqUKq"
    "p6OaKxPcBZAqdRa4sztgc4EzgbspXzgTevNx5dWLb6lYGcvlO1gSPbYDdrCns3sHcDezc7"
    "s3ezFfK714sIzgVfuA/BxORlzRHHUnVJhsr1IPlG9PEdL7Yar7VODQgVngeJYHR0heu86p"
    "zzOUjUCGUqxMrzYeIAyVCZDG3k81yGManbl+Uc4d3xwz3Xf0/v1SwwVHSq6N+/iQnQvt3t"
    "WIH2HR7tc40NA5v3hMBuNbDR4OGdyT3cpL3xsDjfkV9GKqpzVl1Zo92CIVRqqNRQqRua0K"
    "FS72lgoVLvb6X+iDzCoVCW6URXWaMfslZQoKFAQ4FuaB6HAr2ngV0r0M04Gd/X98L5Y+NT"
    "xaFF1Ru3sQe0QI1rgfrYs/SlqgGKNJXtD0ptGtP87FHn84Ont+U9zVfs+ZZqFV8tkVf61n"
    "LssivLmD/1j5qNicnEA947O6vALF7F3KpQuOIF3gt1+WwolkYNECPz3QTwuNv9DgC5VSmA"
    "Uqf4KoYoOrD3d9NJxVcxRNl6WTpr/deyLb+hJbsCPzHf6sJSrCGFxkn8wdYLy9P/PKgtmQ"
    "=="
)
