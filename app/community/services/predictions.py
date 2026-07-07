import random

from app.community.models import Predictions


async def add_prediction(prediction: str) -> Predictions:
    return await Predictions.create(text=prediction)


async def read_all_predictions() -> list[Predictions]:
    return await Predictions.all()


async def read_random_prediction() -> str:
    predictions = await read_all_predictions()
    if not predictions:
        return "Žiadne predpovede v databáze."
    return random.choice(predictions).text


async def update_prediction_by_id(prediction_id: int, text: str) -> None:
    await Predictions.filter(id=prediction_id).update(text=text)


async def delete_prediction_by_id(prediction_id: int) -> None:
    await Predictions.filter(id=prediction_id).delete()
