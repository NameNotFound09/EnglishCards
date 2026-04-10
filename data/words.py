import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Words(SqlAlchemyBase):
    __tablename__ = 'words'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    word = sqlalchemy.Column(sqlalchemy.String)
    translation = sqlalchemy.Column(sqlalchemy.Integer)

