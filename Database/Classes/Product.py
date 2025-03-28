import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.types as satypes
from Database.Classes.Manager import Base

class Product(Base):
    __tablename__ = 'Products'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    name: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
    weight: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
    order_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey('Orders.id'))
    order: orm.Mapped["Order"] = orm.relationship("Order", back_populates="products")
