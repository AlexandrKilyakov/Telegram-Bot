from sqlalchemy import Integer, Column, String, sql, ForeignKey

from utils.db_api.database import BaseModel


class Types(BaseModel):
    __tablename__ = 'types'
    post_id = Column(ForeignKey('books.post_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    types = Column(String(7), primary_key=True)
    url = Column(String(200))
    chapter = Column(String(10))

    query: sql.Select