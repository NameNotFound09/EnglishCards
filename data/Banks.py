import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Bank(SqlAlchemyBase):
    __tablename__ = 'banks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    bank = sqlalchemy.Column(sqlalchemy.JSON)
