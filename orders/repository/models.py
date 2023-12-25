from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from uuid import uuid4


Base = declarative_base()


def make_id():
    return str(uuid4())


class OrderItem(Base):
    __tablename__ = "order_item"
    id = Column(Integer, primary_key=True, nullable=False)
    product = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    quantity = Column(Integer)
    order_id = Column(String, ForeignKey("order.id"))

    def dict(self):
        return {
            "product": self.product,
            "size": self.size,
            "quantity": self.quantity,
        }


class Order(Base):
    __tablename__ = "order"
    id = Column(String, default=make_id, primary_key=True, nullable=False)
    created = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    order = relationship("OrderItem", uselist=False)

    def dict(self):
        return {
            "id": self.id,
            "created": self.created,
            "status": self.status,
            "order": self.order.dict(),
        }
