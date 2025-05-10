import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.types as satypes
from Database.Engine.Engine import Base

class Product(Base):
    __tablename__ = 'Products'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    imageSrc: orm.Mapped[str] = orm.mapped_column(satypes.String(30), nullable=True)
    name: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
    minWeight: orm.Mapped[int] = orm.mapped_column(satypes.Integer(), nullable=True)
    pricePerKg: orm.Mapped[float] = orm.mapped_column(satypes.Float())
    visible: orm.Mapped[bool] = orm.mapped_column(satypes.Boolean())

    def to_json(self):
        return {
            "id": self.id,
            "imageSrc": self.imageSrc,
            "price": self.pricePerKg,
            "name": self.name,
            "minWeight": self.minWeight
        }