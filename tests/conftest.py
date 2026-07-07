import pytest
from tortoise import Tortoise

from app.core.postgres import TORTOISE_ORM


@pytest.fixture(autouse=True)
async def db_setup():
    test_config = {
        "connections": {"default": "sqlite://:memory:"},
        "apps": TORTOISE_ORM["apps"],
        "use_tz": True,
        "timezone": "UTC",
    }
    await Tortoise.init(config=test_config)
    for models in Tortoise.apps.values():
        for model in models.values():
            model._meta.schema = None
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()
