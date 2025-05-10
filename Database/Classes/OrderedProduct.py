import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.types as satypes
from .Product import Product
from .Promocode import Promocode
from Database.Engine.Engine import Base

class OrderedProduct(Base):
    __tablename__ = 'OrderedProducts'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    product_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey('Products.id'), nullable=True)
    product: orm.Mapped[Product] = orm.relationship('Product')
    weight: orm.Mapped[float] = orm.mapped_column(satypes.Float())
    quantity: orm.Mapped[int] = orm.mapped_column(satypes.Integer())
    order_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey('Orders.id'))

    def to_json(self):
        return {
            "id": self.product.id,
            "name": self.product.name,
            "pricePerKg": self.product.pricePerKg,
            "imageSrc": self.product.imageSrc,
            "weight": self.weight,
            "quantity": self.quantity
        }