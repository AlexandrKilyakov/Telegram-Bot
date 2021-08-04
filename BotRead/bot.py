from utils.set_bot_commands import set_default_commands
from loader import db
from utils.db_api import database
from handlers.users.parsing import parsing_sites

async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    print("Подключаем БД")
    await database.on_startup(dp)
    print("Готово")

    print("Создаем таблицы")
    await db.gino.create_all()

    print("Готово")
    await on_startup_notify(dp)
    await set_default_commands(dp)

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    dp.loop.create_task(parsing_sites(21600))
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)