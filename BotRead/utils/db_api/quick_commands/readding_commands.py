from asyncpg import UniqueViolationError
from typing import List
from sqlalchemy import and_

from utils.db_api.schemas.books import Books
from utils.db_api.schemas.readding import Readding
from utils.db_api.schemas.types import Types

#============================================
#ФУНКЦИИ ДЛЯ РАБОТЫ С ТАБЛИЦЕЙ "ЧИТАЮ/СЛЕЖУ"
#============================================

async def add_read(user_id: int, read: int):
    try:
        name = (await Books.select('name').where(Books.post_id == read).gino.first())[0]
        item = Readding(user_id=user_id, read=read, name=name)
        await item.create()
        return True

    except UniqueViolationError:
        return False

async def add_watch(user_id: int, read: int):
    try:
        await Readding.update.values(watch=read).where(and_(Readding.user_id==user_id, 
                                                            Readding.read==read)).gino.status()

    except UniqueViolationError:
        pass

async def delete_item_read(user_id: int, read: int):
    delete = await Readding.delete.where(and_(Readding.user_id==user_id, 
                                              Readding.read==read)).gino.status()
    return delete

async def delete_item_watch(user_id: int, read: int):
    try:
        await Readding.update.values(watch=None).where(and_(Readding.user_id==user_id, 
                                                            Readding.read==read)).gino.status()

    except UniqueViolationError:
        pass

async def delete_all_watch(watch: int):
    await Readding.update.values(watch=None).where(Readding.watch==watch).gino.status()

async def get_user_id(watch: int) -> List[Readding]:
    return await Readding.select('user_id', 'name').where(Readding.watch==watch).gino.all()

async def get_post_id(user_id: int) -> List[Readding]:
    return await Readding.select('read').where(Readding.user_id==user_id).gino.all()

async def get_post_information(user_id: int) -> List[Readding]:
    return await Readding.select('read', 'name').where(Readding.user_id==user_id).order_by(Readding.name.asc()).gino.all()

async def get_post_trackes(user_id: int) -> List[Readding]:
    return await Readding.select('watch', 'name').where(and_(Readding.user_id==user_id, 
                                                             Readding.watch!=None)).order_by(Readding.name.asc()).gino.all()

async def check_post_watch(watch: int):
    item = await Types.query.where(Types.post_id == watch).gino.first()
    return bool(item)