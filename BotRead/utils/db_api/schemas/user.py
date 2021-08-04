from sqlalchemy import Integer, Column, BigInteger, String, sql

from utils.db_api.database import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, unique=True)
    name = Column(String(100))
    status = Column(Integer)
    watch = Column(Integer, nullable=True)

    query: sql.Select