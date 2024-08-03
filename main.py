from aiogram import Dispatcher, Router
from handlers.user_handler import user_router
from instance import bot
import asyncio


def register_router(dp: Dispatcher, router: Router) -> None:
    dp.include_router(router)


async def main() -> None:
    dp = Dispatcher()

    register_router(dp, user_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
