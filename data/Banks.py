import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Bank(SqlAlchemyBase):
    __tablename__ = 'banks'

    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), primary_key=True)
    bank = sqlalchemy.Column(sqlalchemy.JSON)
