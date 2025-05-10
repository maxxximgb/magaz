import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.types as satypes
from .Promocode import Promocode
from .OrderedProduct import OrderedProduct
from Database.Engine.Engine import Base

class Order(Base):
    __tablename__ = 'Orders'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    customer_name: orm.Mapped[str] = orm.mapped_column(satypes.String(30), nullable=True)
    customer_phone: orm.Mapped[str] = orm.mapped_column(satypes.String(30), nullable=True)
    products: orm.Mapped[list[OrderedProduct]] = orm.relationship("OrderedProduct")
    promocode_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey('Promocodes.id'), nullable=True)
    promocode: orm.Mapped[Promocode] = orm.relationship("Promocode")

    def to_json(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "products": [product.to_json() for product in self.products],
            "promocode": self.promocode.to_json() if self.promocode else ""
        }