from repository.models import Order as OrderModel
from repository.models import OrderItem as OrderItemModel
from service.order import Order


class OrderRepository:
    def __init__(self, session):
        self.session = session

    def add(self, **filters):
        order_item = OrderItemModel(product=filters["product"],
                                    size=filters["size"],
                                    quantity=filters["quantity"])
        order = OrderModel(id=filters["id"],
                           created=filters["created"],
                           status=filters["status"],
                           order=order_item)
        self.session.add(order)
        ordering = Order(order)
        return ordering

    def list(self, **filters):
        query_set = self.session.query(OrderModel).all()
        if len(query_set) > 0:
            orders = [Order(order).dict() for order in query_set]
        else:
            orders = []
        if filters["cancelled"] is None and filters["limit"] is None:
            return orders
        if filters["cancelled"] is not None:
            if filters["cancelled"] is True:
                query_set = [
                    Order(order).dict() for order in query_set if order.status == "cancelled"]
            else:
                query_set = [
                    Order(order).dict() for order in query_set if order.status != "cancelled"]
        if filters["limit"] is not None:
            query_set = query_set[:filters["limit"]]
        return query_set

    def delete(self, order):
        self.session.delete(order)

    def update_order_part(self, order, **filters):
        for k, v in filters.items():
            order.order.k = v
        self.session.add(order)
        ordering = Order(order)
        return ordering

    def update_status(self, order, **filters):
        order.status = filters["status"]
        self.session.add(order)
        ordering = Order(order)
        return ordering

    def search(self, order_id):
        order = self.session.query(OrderModel).filter(
            OrderModel.id == order_id).first()
        return order
