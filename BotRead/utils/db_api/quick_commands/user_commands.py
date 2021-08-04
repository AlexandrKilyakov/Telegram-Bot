from asyncpg import UniqueViolationError

from utils.db_api.database import db
from utils.db_api.schemas.user import User
from filters.functions import subscribe

#============================================
#ФУНКЦИИ ДЛЯ РАБОТЫ С ТАБЛИЦЕЙ "ПОЛЬЗОВАТЕЛИ"
#============================================

async def add_user(id: int, name: str, status: int):
    try:
        user = User(id=id, name=name, status=status, watch=None)
        await user.create()

    except UniqueViolationError:
        pass

async def select_all_users():
    users = await User.query.gino.all()
    return users

async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user

async def count_users():
    total = await db.func.count(User.id).gino.scalar()
    return total

async def update_user_status(id, status):
    user = await User.get(id)
    await user.update(status=status).apply()

async def status_user(user_id: int):
    user = await User.query.where(User.id == user_id).gino.first()
    subStatus = await subscribe(user_id)
    if (user.status != int(subStatus)):
        await update_user_status(user_id, int(subStatus))
        
    return int(subStatus)

async def get_active_watch(user_id: int):
    return (await User.select('watch').where(User.id==user_id).gino.first())[0]

async def update_user_active(user_id: int, watch: int = None):
    await User.update.values(watch=watch).where(User.id==user_id).gino.status()