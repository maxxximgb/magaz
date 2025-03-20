import datetime
import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.types as satypes
from Database.Manager import Base

class Promocode(Base):
    __tablename__ = 'Promocodes'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    name: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
    expiration_date: orm.Mapped[satypes.DateTime] = orm.mapped_column(default=datetime.datetime.now())
