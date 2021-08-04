from asyncpg import UniqueViolationError
from typing import List
from sqlalchemy import and_

from utils.db_api.schemas.books import Books
from utils.db_api.schemas.types import Types

#============================================
#ФУНКЦИИ ДЛЯ РАБОТЫ С ТАБЛИЦЕЙ "ЧТИВО"
#============================================

listRandom = []

async def add_books(post_id: int, name: str):
    try:
        global listRandom
        item = Books(post_id=post_id, name=name)
        await item.create()
        listRandom.clear()

    except UniqueViolationError:
        pass

# async def select_all_books() -> List[Books]:
#     return await Books.select('post_id', 'name').gino.all()

async def delete_item_books(post_id: int):
    await Books.delete.where(Books.post_id==post_id).gino.status()

async def check_post(post_id: int):
    user = await Books.query.where(Books.post_id == post_id).gino.first()
    return not bool(user)

async def get_post_id() -> List[Books]:
    global listRandom
    if not listRandom:
        listRandom = await Books.select('post_id').distinct(Books.post_id).gino.all()
    return listRandom

#============================================
#ФУНКЦИИ ДЛЯ РАБОТЫ С ТАБЛИЦЕЙ "TYPES"
#============================================

async def add_types(post_id: int, types: str, url: str, chapter: str):
    try:
        item = Types(post_id=post_id, types=types, url=url, chapter=chapter)
        await item.create()

    except UniqueViolationError:
        pass

async def select_all_types() -> List[Types]:
    return await Types.select('post_id', 'types', 'url', 'chapter').gino.all()

async def update_chapter_types(post_id: int, types: str, chapter: str):
    try:
        await Types.update.values(chapter=chapter).where(and_(Types.post_id==post_id, 
                                                            Types.types==types)).gino.status()
    except UniqueViolationError:
        pass

async def delete_item_types(post_id: int, types: str):
    return await Types.delete.where(and_(Types.post_id==post_id, 
                                            Types.types==types)).gino.status()