from sqlalchemy import Integer, Column, BigInteger, String, sql, ForeignKey

from utils.db_api.database import BaseModel


class Readding(BaseModel):
    __tablename__ = 'readding'
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    read = Column(ForeignKey('books.post_id', ondelete='CASCADE'), primary_key=True, nullable=False)
    name = Column(String(50))
    watch = Column(Integer, nullable=True)

    query: sql.Select