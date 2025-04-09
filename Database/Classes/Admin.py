import sqlalchemy.orm as orm
import sqlalchemy.types as satypes
from Database.Engine.Engine import Base

class Admin(Base):
    __tablename__ = 'Admins'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    login: orm.Mapped[str] = orm.mapped_column(satypes.String(30), unique=True)
    surname: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
    name: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
    hashed_password: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
