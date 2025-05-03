import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.types as satypes
from Database.Engine.Engine import Base

class Product(Base):
    __tablename__ = 'Products'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    imageSrc: orm.Mapped[str] = orm.mapped_column(satypes.String(30), nullable=True)
    name: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
    weight: orm.Mapped[int] = orm.mapped_column(satypes.Integer(), nullable=True)
    price: orm.Mapped[int] = orm.mapped_column(satypes.Integer())
    visible: orm.Mapped[bool] = orm.mapped_column(satypes.Boolean())
    order_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey('Orders.id'), nullable=True)

    def to_json(self):
        return {
            "id": self.id,
            "imageSrc": self.imageSrc,
            "price": self.price,
            "name": self.name,
            "weight": self.weight
        }