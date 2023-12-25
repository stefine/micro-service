from server import create_server
from repository.orders_repository import OrderRepository
from service.order_service import OrderService


server = create_server(OrderRepository, OrderService)

from api import api
