from app.models import Warnings


async def create_warning(user_id: int, reason: str) -> Warnings:
    return await Warnings.create(
        user_id=user_id,
        reason=reason,
    )


async def read_all_warnings() -> list[Warnings]:
    return await Warnings.all()


async def read_all_warnings_by_user_id(user_id: int) -> list[Warnings]:
    return await Warnings.filter(user_id=user_id).all()


async def delete_all_warnings() -> None:
    await Warnings.all().delete()


async def delete_all_warnings_by_user_id(user_id: int) -> None:
    await Warnings.all().filter(user_id=user_id).delete()


async def delete_last_warning_by_user_id(user_id: int) -> None:
    last_warning = await Warnings.filter(user_id=user_id).latest("created_at")
    if last_warning:
        await last_warning.delete()
