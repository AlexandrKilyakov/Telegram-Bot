from sqlalchemy import Integer, Column, String, sql

from utils.db_api.database import BaseModel


class Books(BaseModel):
    __tablename__ = 'books'
    post_id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50))

    query: sql.Select