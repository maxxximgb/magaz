import datetime
import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.types as satypes

Base = orm.declarative_base()

class Admin(Base):
    __tablename__ = 'Admins'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    login: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
    surname: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
    name: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
    position: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
    hashed_password: orm.Mapped[str] = orm.mapped_column(satypes.String(30))

class Product(Base):
    __tablename__ = 'Products'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    name: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
    weight: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
    order_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey('Orders.id'))
    order: orm.Mapped["Order"] = orm.relationship("Order", back_populates="products")

class Promocode(Base):
    __tablename__ = 'Promocodes'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    name: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
    expiration_date: orm.Mapped[satypes.DateTime] = orm.mapped_column(default=datetime.datetime.now())

class Order(Base):
    __tablename__ = 'Orders'
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    weight: orm.Mapped[str] = orm.mapped_column(satypes.String(30))
    products: orm.Mapped[list[Product]] = orm.relationship("Product", back_populates="order")
    promocode_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey('Promocodes.id'), nullable=True)
    promocode: orm.Mapped[Promocode] = orm.relationship("Promocode")

