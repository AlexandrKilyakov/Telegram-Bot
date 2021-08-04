from data.config import CHANNEL_ID
from loader import bot

# ===========================================================================================
# Проверка, является ли человек подписчиком
# ===========================================================================================
async def subscribe(user_id):
    return ((await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)).status != "left")