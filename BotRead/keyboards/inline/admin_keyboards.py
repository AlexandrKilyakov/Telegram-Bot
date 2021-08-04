from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#МЕНЮ АДМИНА
admin_buttons = InlineKeyboardMarkup(inline_keyboard=[
	[
		InlineKeyboardButton(text="📔 Чтение", callback_data="Books")
	]
])