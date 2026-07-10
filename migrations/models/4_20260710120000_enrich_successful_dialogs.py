from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "llm"."successful_dialogs" ADD COLUMN IF NOT EXISTS "thread_id" BIGINT;
        ALTER TABLE "llm"."successful_dialogs" ADD COLUMN IF NOT EXISTS "user_id" BIGINT;
        ALTER TABLE "llm"."successful_dialogs" ADD COLUMN IF NOT EXISTS "topic" TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "llm"."successful_dialogs" DROP COLUMN IF EXISTS "thread_id";
        ALTER TABLE "llm"."successful_dialogs" DROP COLUMN IF EXISTS "user_id";
        ALTER TABLE "llm"."successful_dialogs" DROP COLUMN IF EXISTS "topic";"""


MODELS_STATE = (
    "eJztWltz2joQ/isMT+lM2iHkQnreIOW0dAJkEnqZds54hC2MGltyLbkJ0+a/H0m+G+HUNC"
    "kG9Gb2gqVvrd1vJf1susSCDn3VI+waeg6CtPlP42cTAxfyB4X2sNEEnpfqhICBqSPNp4QZ"
    "fsZwSpkPTMZVM+BQyEUWpKaPPIYI5lIcOI4QEpMbImynogCj7wE0GLEhm0OfK77+x8UIW/"
    "BejlH+9G6NGYKOlRszssS7pdxgC0/KesgeYPavtBUvnBomcQIXp/begs0JThwQZkJqQwx9"
    "wKB4A/MDMQMxwGi+8aTCwaYm4SgzPhacgcBhmRn/JgwmwQJCPpowLrZ4y8vX7fbxcafdOj"
    "47Pz3pdE7PW+fcVg5pWdV5CCecAhL+lYRl8HYwmoiJEh6nMIZC8CB9AAOhl8Q7Bdj0oYDE"
    "AGwZ6Ddcw5AL1VDnPQuQW5Hrq/ihGIAY7rIIxII0BOmX90Qx4HOwxthZROEtgXcyGPZvJt"
    "3hlZiJS+l3R0LUnfSFpi2li4L04OxFPh7JnzQ+DSbvGuJn48t41JcIEspsX74xtZt8aYox"
    "gYARA5M7A1iZLzGWxsBwy0xg54AZVZdPxunxNVSTEP7FZZTJpZBSYMPKAOf91sI4Cv7OQ8"
    "zmYnFWRjjnpgEuAZgPgsF7Rd6fcOmK/JC6FKDl06lnfihL6f3Pk1w2H33sXl+8614fDLuf"
    "X+Qy+uV49DY2TzEdXVyOewVUBWVaVME0cdCIqhGlgWnytKlIA4Q4EGA1rBmvArBT7lbLNF"
    "C2osfjyxywvUERuQ/DXv/64EiizI0QW7HseXo0xcgUgK5Mqjmfv8cMWn+cUttHJ52T8+Oz"
    "kySTJpKyBLqMGjWJvxZNzjk+AUuu1WdZJ1IcT3uJFYvmcnab6X6EYArM2zvgW8aShrTJKt"
    "tlldt2ixKAOcGzIjTFOKO+exhSP2VPnugOyzpyN2ul23Hdjut2vBaZR7fjm25lNtiO7w3G"
    "uh9/ZoADCv3K8GacNLiPgCufl9Bd3ZlnfdZqzuvF1Z+jN6+6gaR3jx7Z64CYrdNkpm7byf"
    "y2hOnVvce8CTe9ZoHzBgGH2Mpmc9nosKzrpIm5YWXsdf+p+0/df9YiK+n+c9PsUh+l6aO0"
    "bUBUHkZUOPdJ7PfmzKcmRO4Dbz2vfDJDjvrAIKcvpW9yg8DLmmrmppmbZm5bw9w2si2404"
    "tI7wo+M82A2OZlzRWbUlUZh8p1b8hHkfwiSHmxNXitdStAqPDcSwSjjStY5aJTzmcvUXMA"
    "5UsPQlyVRuQc9UWn/d2Efk9u1U1LqDgs61a+JSa6S9legqW7lP3rUjxrzcDmPXVgNxrYaP"
    "D6gP8pW6Oa1OUrH1oousavqM5ZdWmN9gqGulLrSq0rdU0Tuq7UOxpYXal3t1J/Aj7mUCjL"
    "dKIrrdF3WStdoHWB1gW6pnlcF+gdDexSga7HQe6uXsHjnw0likOLsttisYemQLWjQF3oI3"
    "OuIkCRppT+gNSmNuRnh5jPHx42ruY0P6BPkWoVX8yBr0Yv47Ity5h/9feGA7HNxAfePj0t"
    "wSxexdyqULjiBd4OdflsKJZGBRAj8+0E8KjV+g0AudVKAKVOcaMbKxjY+5vxqORGN1ZSL2"
    "Syxq+Gg2hNS3YJfmK+5YWlWEMKxEn8wcYLy8P/uOhBhQ=="
)
