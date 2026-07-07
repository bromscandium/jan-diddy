from dataclasses import dataclass

import pytest
from polyfactory.factories.dataclass_factory import DataclassFactory

from app.community.services import jokes, predictions, warnings


@dataclass
class WarningData:
    user_id: int
    reason: str

@dataclass
class TextData:
    text: str

class WarningFactory(DataclassFactory[WarningData]):
    __model__ = WarningData

class TextFactory(DataclassFactory[TextData]):
    __model__ = TextData

@pytest.mark.asyncio
async def test_create_warning_with_polyfactory():
    fake = WarningFactory.build()
    await warnings.create_warning(fake.user_id, fake.reason)
    user_warnings = await warnings.read_all_warnings_by_user_id(fake.user_id)
    assert len(user_warnings) == 1
    assert user_warnings[0].reason == fake.reason

@pytest.mark.asyncio
async def test_delete_user_warnings():
    fake = WarningFactory.build()
    await warnings.create_warning(fake.user_id, fake.reason)
    await warnings.delete_all_warnings_by_user_id(fake.user_id)
    user_warnings = await warnings.read_all_warnings_by_user_id(fake.user_id)
    assert len(user_warnings) == 0

@pytest.mark.asyncio
async def test_read_random_joke_empty():
    res = await jokes.read_random_joke()
    assert res == "Žiadne žarty v databáze."

@pytest.mark.asyncio
async def test_read_random_joke_populated():
    fake = TextFactory.build()
    await jokes.add_joke(fake.text)
    res = await jokes.read_random_joke()
    assert res == fake.text

@pytest.mark.asyncio
async def test_read_random_prediction_empty():
    res = await predictions.read_random_prediction()
    assert res == "Žiadne predpovede v databáze."

@pytest.mark.asyncio
async def test_read_random_prediction_populated():
    fake = TextFactory.build()
    await predictions.add_prediction(fake.text)
    res = await predictions.read_random_prediction()
    assert res == fake.text
