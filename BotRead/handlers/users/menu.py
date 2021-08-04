from random import randrange
from aiogram import types
from aiogram.dispatcher.filters.builtin import Command

from loader import dp, bot
from utils.db_api import quick_commands as commands
from utils.db_api.quick_commands import readding_commands
from keyboards.inline.menu_keyboards import *
from data.config import CHANNEL_ID
# from typing import List

menuText = "Для вас доступны следующие возможности:"

# ------------------------------------------------------------------------------------------------------------------------------
# МЕНЮ
# ------------------------------------------------------------------------------------------------------------------------------
@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
	if await commands.user_commands.status_user(user_id=message.from_user.id):
		await message.answer(text=menuText, reply_markup=menu_for_subscribers)
	else:
		await message.answer(text=menuText, reply_markup=regular_menu)

# ------------------------------------------------------------------------------------------------------------------------------
# РАНДОМ
# ------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text_contains="Random")
async def random_readding(call: types.CallbackQuery):
	await call.answer(cache_time=3)

	await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

	listRandom = await commands.books_commands.get_post_id();
	listReadding = await readding_commands.get_post_id(user_id=call.from_user.id);

	if listReadding:
		listRandom = [item for item in listRandom if item not in listReadding]

	if listRandom:
		post_id = listRandom[randrange(len(listRandom))][0]
		await commands.user_commands.update_user_active(user_id=call.from_user.id, watch=int(post_id))
		await bot.forward_message(from_chat_id=CHANNEL_ID, chat_id=call.from_user.id, message_id=post_id)

	if listRandom:
		await call.message.answer(text="🧐 Заинтересовало?", reply_markup=random_menu_active)
	else:
		await call.message.answer(text="На данный момент, вы всё прочитали 👍. Ждём обновления на канале! 😉", reply_markup=empty_menu)

# ------------------------------------------------------------------------------------------------------------------------------
# ДОБАВИТЬ В СПИСОК "ЧИТАЮ"
# ------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text_contains="RanRead")
async def added_to_the_list(call: types.CallbackQuery):
	try:
		if await commands.readding_commands.add_read(user_id=call.from_user.id, read=await commands.user_commands.get_active_watch(user_id=call.from_user.id)):
			await call.answer(text="Добавлен в список.")
		else:
			await call.answer(text="Вы уже добавили!")
	except:
		await call.answer(text="Нажмите на другую кнопку!")

	await call.answer(cache_time=3)

# ------------------------------------------------------------------------------------------------------------------------------
# ДОБАВИТЬ В СПИСОК "ОТСЛЕЖИВАЮ"
# ------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text_contains="ITracked")
async def tracked_added_to_the_list(call: types.CallbackQuery):
	try:
		post_id = await commands.user_commands.get_active_watch(user_id=call.from_user.id)
		if await readding_commands.check_post_watch(watch=post_id):
			await commands.readding_commands.add_watch(user_id=call.from_user.id, read=int(post_id))
			await call.answer(text="Добавлен в список.")
		else:
			await call.answer(text="Этот тайтл уже завершился. Или есть другая причина его не отслеживать.")
	except:
		await call.answer(text="Нажмите на другую кнопку!")

	await call.answer(cache_time=3)

# ------------------------------------------------------------------------------------------------------------------------------
# ЧИТАЮ
# ------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text_contains="Readding")
async def show_item_list(call: types.CallbackQuery):
	await call.answer(cache_time=3)
	await list_readding(call=call)

# РЕПОСТЫ ПО КНОПКЕ
@dp.callback_query_handler(choice_callback.filter(item_name=["Read", "Watch"]))
async def show_selected_post(call: types.CallbackQuery, callback_data: dict):
	await call.answer(cache_time=1)
	post_id = callback_data.get("post_url")
	item_name = callback_data.get("item_name")

	await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
	await bot.forward_message(from_chat_id=CHANNEL_ID, chat_id=call.from_user.id, message_id=post_id)

	await commands.user_commands.update_user_active(user_id=call.from_user.id, watch=int(post_id))

	await call.message.answer(text="Это то, что вы искали? 🧐", reply_markup=tracked_submenu if item_name == "Watch" else readding_submenu)


# РЕПОСТЫ ПО КНОПКЕ
@dp.callback_query_handler(choice_callback.filter(item_name="ParsW"))
async def show_parsing_post(call: types.CallbackQuery, callback_data: dict):
	await call.answer(cache_time=1)
	post_id = callback_data.get("post_url")

	await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
	await bot.forward_message(from_chat_id=CHANNEL_ID, chat_id=call.from_user.id, message_id=post_id)

# СПИСОК ДЛЯ ЧТЕНИЯ
@dp.callback_query_handler(list_callback.filter(item_name=["ReadLevel"]))
async def navigation_list(call: types.CallbackQuery, callback_data: dict):
	await call.answer(cache_time=1)
	level = callback_data.get("level")
	await list_readding(call=call, level=int(callback_data.get("level")))

# УДАЛИТЬ ИЗ БД
@dp.callback_query_handler(delete_callback.filter(item_name=["IDelete"]))
async def navigation_list(call: types.CallbackQuery, callback_data: dict):
	await call.answer(cache_time=1)
	category = callback_data.get("category")

	post_id = await commands.user_commands.get_active_watch(user_id=call.from_user.id)
	await commands.user_commands.update_user_active(user_id=call.from_user.id)

	if category == "delRead":
		await commands.readding_commands.delete_item_read(user_id=call.from_user.id, read=post_id)
		await list_readding(call=call)
	else:
		await commands.readding_commands.delete_item_watch(user_id=call.from_user.id, read=post_id)
		await list_tracked(call=call)

# ------------------------------------------------------------------------------------------------------------------------------
# ОТСЛЕЖИВАТЬ
# ------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text_contains="Track")
async def item_list(call: types.CallbackQuery):
	await call.answer(cache_time=3)
	await list_tracked(call=call)

# СПИСОК ДЛЯ ОТСЛЕЖИВАНИЯ
@dp.callback_query_handler(list_callback.filter(item_name=["TLevel"]))
async def use_navigation_list(call: types.CallbackQuery, callback_data: dict):
	await call.answer(cache_time=1)
	await list_tracked(call=call, level=int(callback_data.get("level")))

# ------------------------------------------------------------------------------------------------------------------------------
# НАЗАД
# ------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text_contains="Level1")
async def cansel_random(call: types.CallbackQuery):
	await call.answer(cache_time=1)

	if await commands.user_commands.status_user(user_id=call.from_user.id):
		await call.message.edit_text(text=menuText, reply_markup=menu_for_subscribers)
	else:
		await call.message.edit_text(text=menuText, reply_markup=regular_menu)

@dp.callback_query_handler(text_contains="Level2.1")
async def cansel_list_items(call: types.CallbackQuery):
	await call.answer(cache_time=1)
	await list_readding(call=call)

@dp.callback_query_handler(text_contains="Level2.2")
async def cansel_list_items(call: types.CallbackQuery):
	await call.answer(cache_time=1)
	await list_tracked(call=call)

# ------------------------------------------------------------------------------------------------------------------------------
# ЧАСТО ИСПОЛЬЗУЮЩИЕСЯ ФУНКЦИИ
# ------------------------------------------------------------------------------------------------------------------------------

# Функция для кнопки "ЧИТАЮ"
async def list_readding(call: types.CallbackQuery, level: int = 0, **kwargs):
	listReadding = await commands.readding_commands.get_post_information(user_id=call.from_user.id);

	if listReadding:
		await create_list_readding(arr=listReadding, number=level)
		await call.message.edit_text(text="В данном списке находятся следующие тайтлы:", reply_markup=readding_menu_active)
	else:
		await call.message.edit_text(text="На данный момент, этот список пуст. 😑", reply_markup=empty_menu)

# Функция для кнопки "ОТСЛЕЖИВАЮ"
async def list_tracked(call: types.CallbackQuery, level: int = 0, **kwargs):
	listReadding = await commands.readding_commands.get_post_trackes(user_id=call.from_user.id);

	if listReadding:
		await create_list_tracked(arr=listReadding, number=level)
		await call.message.edit_text(text="В данном списке находятся следующие тайтлы:", reply_markup=tracked_menu_active)
	else:
		await call.message.edit_text(text="На данный момент, этот список пуст. 😑", reply_markup=empty_menu)