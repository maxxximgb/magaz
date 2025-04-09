import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.types as satypes
from .Product import Product
from .Promocode import Promocode
from Database.Engine.Engine import Base

class Order(Base):
    __tablename__ = 'Orders'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    weight: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
    products: orm.Mapped[list[Product]] = orm.relationship("Product", back_populates="order")
    promocode_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey('Promocodes.id'), nullable=True)
    promocode: orm.Mapped[Promocode] = orm.relationship("Promocode")
