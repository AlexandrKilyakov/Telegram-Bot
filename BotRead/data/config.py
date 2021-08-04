import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("TOKEN_BOT"))
CHANNEL_ID = str(os.getenv("CHANNEL_ID"))
URL_CHANNEL = str(os.getenv("URL_CHANNEL"))
URL_AUTHOR = str(os.getenv("URL_AUTHOR"))

PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))

admins = [
    os.getenv("ADMIN_ID"),
]

ip = os.getenv("ip")

# Ссылка подключения к базе данных
POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}"

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
