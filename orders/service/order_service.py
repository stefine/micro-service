from uuid import uuid4
from datetime import datetime


class OrderService:
    def __init__(self, repo):
        self.repo = repo

    def place_order(self, payload):
        order = payload.dict()["order"]
        order = self.repo.add(id=str(uuid4()),
                              created=datetime.utcnow(),
                              status="created",
                              product=order["product"],
                              size=order["size"].value,
                              quantity=order["quantity"])
        return order

    def list_orders(self, **filters):
        orders = self.repo.list(**filters)
        return orders

    def delete_order(self, order):
        self.repo.delete(order)

    def update_order(self, order, payload):
        order_new = payload.dict()["order"]
        filters = {"size": order_new["size"].value,
                   "product": order_new["product"],
                   "quantity": order_new["quantity"]}
        order = self.repo.update_order_part(order, **filters)
        return order

    def search_order(self, order_id):
        order = self.repo.search(order_id)
        return order

    def update_order_status(self, order, status):
        order = self.repo.update_status(order, status=status)
        return order
