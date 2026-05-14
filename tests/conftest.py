import pytest
from tortoise import Tortoise

from app.db.postgres import TORTOISE_ORM


@pytest.fixture(autouse=True)
async def db_setup():
    # Use SQLite in-memory for fast tests
    test_orm_config = TORTOISE_ORM.copy()
    test_orm_config["connections"]["default"] = "sqlite://:memory:"
    
    await Tortoise.init(config=test_orm_config)
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()
