import sqlalchemy
import sqlalchemy.orm as orm
from .Product import Product
from .Promocode import Promocode
from Database.Engine.Engine import Base

class Order(Base):
    __tablename__ = 'Orders'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    products: orm.Mapped[list[Product]] = orm.relationship("Product")
    promocode_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey('Promocodes.id'), nullable=True)
    promocode: orm.Mapped[Promocode] = orm.relationship("Promocode")

    def to_json(self):
        return {
            "id": self.id,
            "products": [product.to_json() for product in self.products],
            "promocode": self.promocode.to_json()
        }