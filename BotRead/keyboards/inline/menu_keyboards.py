from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from data.config import URL_AUTHOR, URL_CHANNEL

choice_callback = CallbackData("choice", "item_name", "post_url")
list_callback = CallbackData("choice", "item_name", "level")
delete_callback = CallbackData("delete", "item_name", "category")

menu_for_subscribers = InlineKeyboardMarkup(row_width=1)
regular_menu = InlineKeyboardMarkup(row_width=1)
random_menu_active = InlineKeyboardMarkup(row_width=2)
readding_menu_active = InlineKeyboardMarkup(row_width=1)
readding_submenu = InlineKeyboardMarkup(row_width=2)
tracked_menu_active = InlineKeyboardMarkup(row_width=1)
tracked_submenu = InlineKeyboardMarkup(row_width=2)
empty_menu = InlineKeyboardMarkup(row_width=1)
search_menu = InlineKeyboardMarkup(row_width=3)

# Первое меню
random = InlineKeyboardButton(text="🎲 Рандом", callback_data="Random")
readding = InlineKeyboardButton(text="📚 Читаю", callback_data="Readding") 
tracked = InlineKeyboardButton(text="👀 Отслеживаю", callback_data="Track") 
write = InlineKeyboardButton(text="✏ Написать автору", url=URL_AUTHOR) 
subscribe = InlineKeyboardButton(text="Подписаться на канал", url=URL_CHANNEL)

# Второе меню
rondomRead = InlineKeyboardButton(text="📚 Читать", callback_data="RanRead")

# Кнопки назад
CancelRandom = InlineKeyboardButton(text="👈 Назад", callback_data="Level1")
CancelReadding = InlineKeyboardButton(text="👈 Назад", callback_data="Level2.1")
CancelTracked = InlineKeyboardButton(text="👈 Назад", callback_data="Level2.2")

empty_menu.insert(CancelRandom)

# ===================================
# Меню первого уровня
# ===================================
menu_for_subscribers.insert(random)
menu_for_subscribers.row(readding, tracked)
menu_for_subscribers.insert(write)

regular_menu.insert(random)
regular_menu.insert(subscribe)

# ===================================
# Меню второго уровня
# ===================================

# -----------------------------------
# РАНДОМ
# -----------------------------------
random_menu_active.insert(random)
random_menu_active.insert(rondomRead)
random_menu_active.insert(CancelRandom)

# ===================================
# Меню третьего уровня
# ===================================
readding_submenu.insert(InlineKeyboardButton(text="🔔 Отслеживать", callback_data="ITracked"))
readding_submenu.insert(InlineKeyboardButton(text="♻ Удалить", callback_data=delete_callback.new(item_name="IDelete", category="delRead")))
readding_submenu.insert(CancelReadding)

tracked_submenu.insert(CancelTracked)
tracked_submenu.insert(InlineKeyboardButton(text="♻ Удалить", callback_data=delete_callback.new(item_name="IDelete", category="delWatch")))

# -----------------------------------
# ЧИТАЮ
# -----------------------------------
async def create_list_readding(arr: list = [], number: int = 0):	
	maxLen = len(arr)
	maxX = number * 5

	readding_menu_active.__init__(row_width=1)
	
	if maxX + 5 <= maxLen:
		maxX += 5
	else:
		maxX = maxLen

	minX = (number * 5) if (number > 0) else 0

	for i in range(minX, maxX):
		readding_menu_active.insert(InlineKeyboardButton(text=f"{arr[i][1]}", callback_data=choice_callback.new(item_name="Read", post_url=f"{arr[i][0]}")))

	if minX > 0 and maxX < maxLen:
		readding_menu_active.row(InlineKeyboardButton(text="<<", callback_data=list_callback.new(item_name="ReadLevel", level=number - 1)), 
								 InlineKeyboardButton(text=">>", callback_data=list_callback.new(item_name="ReadLevel", level=number + 1)))
	elif maxX == maxLen and maxLen > 5:
		readding_menu_active.insert(InlineKeyboardButton(text="<<", callback_data=list_callback.new(item_name="ReadLevel", level=number - 1)))
	elif minX == 0 and maxLen > 5:
		readding_menu_active.insert(InlineKeyboardButton(text=">>", callback_data=list_callback.new(item_name="ReadLevel", level=number + 1)))
		
	readding_menu_active.insert(CancelRandom)

# -----------------------------------
# ОТСЛЕЖИВАЮ
# -----------------------------------
async def create_list_tracked(arr: list = [], number: int = 0):	
	maxLen = len(arr)
	maxX = number * 5

	tracked_menu_active.__init__(row_width=1)
	
	if maxX + 5 <= maxLen:
		maxX += 5
	else:
		maxX = maxLen

	minX = (number * 5) if (number > 0) else 0

	for i in range(minX, maxX):
		tracked_menu_active.insert(InlineKeyboardButton(text=f"{arr[i][1]}", callback_data=choice_callback.new(item_name="Watch", post_url=f"{arr[i][0]}")))

	if minX > 0 and maxX < maxLen:
		tracked_menu_active.row(InlineKeyboardButton(text="<<", callback_data=list_callback.new(item_name="TLevel", level=number - 1)), 
								 InlineKeyboardButton(text=">>", callback_data=list_callback.new(item_name="TLevel", level=number + 1)))
	elif maxX == maxLen and maxLen > 5:
		tracked_menu_active.insert(InlineKeyboardButton(text="<<", callback_data=list_callback.new(item_name="TLevel", level=number - 1)))
	elif minX == 0 and maxLen > 5:
		tracked_menu_active.insert(InlineKeyboardButton(text=">>", callback_data=list_callback.new(item_name="TLevel", level=number + 1)))
		
	tracked_menu_active.insert(CancelRandom)