import asyncio
from aiogram import Bot, Dispatcher


async def main() -> None:
    bot: Bot = Bot(token='', parse_mode="HTML")
    dp: Dispatcher = Dispatcher()
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
