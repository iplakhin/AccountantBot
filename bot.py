import asyncio
from aiogram import Bot, Dispatcher
from config.config import Config, load_config
from handlers import handlers
from keyboard.mainmenu import set_main_menu
async def main() -> None:
    config: Config = load_config()
    bot: Bot = Bot(token=config.tgbot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())