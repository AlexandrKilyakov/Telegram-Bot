from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, bot
from utils.db_api.quick_commands import user_commands as commands
from filters.functions import subscribe
from data.config import CHANNEL_ID


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
	name = message.from_user.full_name
	await commands.add_user(id=message.from_user.id, name=name, status=await subscribe(message.from_user.id))

	if await commands.status_user(user_id=message.from_user.id):
		await message.answer(text=f"Примет, {name} 🤗\nЯ могу помочь тебе в поиске интересного чтива 📚. Если что-то выбрал, то скажи мне 🙃, и я буду отслеживать для тебя выходы новых глав.\nВызов меню - '/menu'")
	else:
		await message.answer(text=f"Примет, {name} 🤗\nЯ могу помочь тебе в поиске интересного чтива 📚. А также могу отслеживать выходы новых глав. Но для этого вам <b>необходимо подписаться</b>.\nВызов меню - '/menu'")