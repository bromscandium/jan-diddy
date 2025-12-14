import random

from app.models.jokes import Jokes


async def add_joke(joke: str) -> Jokes:
    return await Jokes.create(text=joke)


async def read_all_jokes() -> list[Jokes]:
    return await Jokes.all()


async def read_random_joke() -> str:
    jokes = await Jokes.all()
    if not jokes:
        return "Žiadne žarty v databáze."
    return random.choice(jokes).text


async def update_joke_by_id(joke_id: int, text: str) -> None:
    await Jokes.filter(id=joke_id).update(text=text)


async def delete_joke_by_id(joke_id: int) -> None:
    await Jokes.filter(id=joke_id).delete()
