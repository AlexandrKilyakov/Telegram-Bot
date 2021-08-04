from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.menu_keyboards import choice_callback
from utils.db_api.quick_commands import books_commands as commands
from utils.db_api.quick_commands import readding_commands
from filters.parsing_functions import get_link_chapter
from loader import bot
import asyncio
from datetime import datetime

async def parsing_sites(wait_for):
	while True:
		await asyncio.sleep(wait_for)

		url_array = await commands.select_all_types()

		for i in range(len(url_array)):
			status = await get_link_chapter(link=url_array[i][2])
			
			if not status:
				await commands.delete_item_types(post_id=int(url_array[i][0]), types=url_array[i][1])
				await readding_commands.delete_all_watch(watch=int(url_array[i][0]))
				continue
			elif status != url_array[i][3]:
				await commands.update_chapter_types(post_id=int(url_array[i][0]), types=url_array[i][1], chapter=status)
				Readding = await readding_commands.get_user_id(watch=int(url_array[i][0]))

				if Readding:
					for j in range(len(Readding)):
						await bot.send_message(text=f"✅ Вам пришло обновление - '{url_array[i][1]}' 😎", chat_id=Readding[j][0], reply_markup=InlineKeyboardMarkup(inline_keyboard=[
																															[
																																InlineKeyboardButton(text=f"{Readding[j][1]}", callback_data=choice_callback.new(item_name="ParsW", post_url=f"{url_array[i][0]}"))
																															]
																														]))
				else:
					continue