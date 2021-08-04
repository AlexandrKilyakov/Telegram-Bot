from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ContentTypes

from keyboards.inline.admin_keyboards import admin_buttons
from states.editTables import addBooks
from loader import dp, bot
from data.config import admins
from filters.forwarded_message import IsForwarded
from utils.db_api.quick_commands import books_commands as commands
from filters.parsing_functions import get_link_chapter

@dp.message_handler(Command("edit"), user_id=admins)
async def edit(message: Message):
	await message.answer(text="Добро пожаловать, хозяин 😌. Что вы хотите сделать сегодня?", reply_markup=admin_buttons)

# ЗАПОЛНЯЕМ ТАБЛИЦУ С НАЗВАНИЕМ 'BOOKS'
@dp.callback_query_handler(text_contains="Books")
async def collect_information(call: CallbackQuery):
	await call.answer(cache_time=3)
	
	await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
	await bot.send_message(text="Отправьте мне пост из канала.", chat_id=call.from_user.id)
	await addBooks.POSTID.set()

#ПОЛУЧАЕМ ДАННЫЕ ИЗ ПОСТА
@dp.message_handler(IsForwarded(), content_types=ContentTypes.ANY, state=addBooks.POSTID)
async def get_post_info(message: Message, state: FSMContext):
	post_id = message.forward_from_message_id

	try:
		if await commands.check_post(post_id=post_id):
			for i in range(len(message.reply_markup.inline_keyboard)):
				for j in range(len(message.reply_markup.inline_keyboard[i])):

					if message.reply_markup.inline_keyboard[i][j]["text"] != "Новелла":
						await state.update_data(name=message.reply_markup.inline_keyboard[i][j]["text"])
						break
					else:
						pass

			await state.update_data(post_id=post_id)

			await message.answer(text="Отправьте мне типы и ссылки в таком формате:\n"
								"<code>Новелла - https://remanga.org | Манга - https://remanga.org</code>\n"
								"Или\n"
								"<code>Новелла - https://remanga.org</code>")
			await addBooks.TYPES.set()
		else:
			await message.answer(text="Этот пост уже есть в базе данных. Начните заново.")
			await state.finish()
	except:
		await state.finish()
		await message.answer(text="Возникла ошибка! Вы отправили правильный пост? 🤔")


#ПОЛУЧАЕМ ПОСЛЕДНЮЮ ИНФУ
@dp.message_handler(state=addBooks.TYPES)
async def answer_q6(message: Message, state: FSMContext):
	example = ""
	text = message.text
	await state.update_data(text=text)
	data = await state.get_data()
	post_id = data.get("post_id")
	name = data.get("name")

	try:
		example += f"<code>{post_id} = {name}</code>"
		
		if ' | ' in text:
			text = text.split(' | ')
			for i in range(len(text)):
				var = text[i].split(' - ')
				example += f"\n<code>{var[0]} = {var[1]}</code>"
		else:
			var = text.split(' - ')
			example += f"\n<code>{var[0]} = {var[1]}</code>"

		await message.answer(text=f"{example}\n\nСохранить эти данные в базу данных? (да/нет)")
		await addBooks.DONE.set()
	except:
		await message.answer(text="Возникла ошибка, попробуйте ещё раз.")
		await state.finish()

#ПОЛУЧАЕМ СОГЛАСИЕ
@dp.message_handler(state=addBooks.DONE)
async def answer_q6(message: Message, state: FSMContext):
	done = message.text
	data = await state.get_data()
	post_id = data.get("post_id")
	name = data.get("name")
	text = data.get("text")

	await state.finish()

	if done in ["Да", "да", "Д", "д"]:
		try:
			await commands.add_books(post_id=post_id, name=name)
			
			if ' | ' in text:
				text = text.split(' | ')
				for i in range(len(text)):
					var = text[i].split(' - ')

					chapter = await get_link_chapter(link=str(var[1]))

					if chapter:
						await commands.add_types(post_id=post_id, types=var[0], url=var[1], chapter=chapter)
			else:
				var = text.split(' - ')

				chapter = await get_link_chapter(link=str(var[1]))

				if chapter:
					await commands.add_types(post_id=post_id, types=var[0], url=var[1], chapter=chapter)

			await message.answer(text="Данные успешно добавлены! 😁")
		except:
			await message.answer(text="Возникла ошибка, попробуйте ещё раз.")
			await commands.delete_item_books(post_id=post_id)
	else:
		await message.answer(text="Вы решили не сохранять эти данные!")