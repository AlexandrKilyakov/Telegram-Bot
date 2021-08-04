from aiogram.dispatcher.filters.state import StatesGroup, State

class addBooks(StatesGroup):
	POSTID = State()
	TYPES = State()	
	DONE = State()	