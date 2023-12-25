# from api.schema import GetOrderSchema, CreateOrderSchema, GetOrdersSchema
from api import GetOrderSchema, CreateOrderSchema, GetOrdersSchema
from run import server
from typing import Optional
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.requests import Request
from repository.unit_of_work import UnitOfWork
from uuid import UUID


orders = []


@server.get("/orders/", response_model=GetOrdersSchema)
def getOrders(request: Request,
              cancelled: Optional[bool] = None, limit: Optional[int] = None):
    with UnitOfWork() as unit_of_work:
        repo = request.app.register_repo(unit_of_work.session)
        order_service = request.app.register_serv(repo)
        orders = order_service.list_orders(cancelled=cancelled, limit=limit)
        return {"orders": orders}  # 空的时候必须要字典形式


@server.post(
    "/orders/",
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema)
def createOrder(request: Request, payload: CreateOrderSchema):
    with UnitOfWork() as unit_of_work:
        repo = request.app.register_repo(unit_of_work.session)
        order_service = request.app.register_serv(repo)
        order = order_service.place_order(payload)
        unit_of_work.commit()
        return order.dict()


@server.get("/orders/{order_id}", response_model=GetOrderSchema)
def getOrderById(request: Request, order_id: UUID):
    with UnitOfWork() as unit_of_work:
        repo = request.app.register_repo(unit_of_work.session)
        order_service = request.app.register_serv(repo)
        order = order_service.search_order(str(order_id))
        if order is None:
            raise HTTPException(
                status_code=404,
                detail=f"Order with ID {order_id} not found"
            )
        return order.dict()


@server.put("/orders/{order_id}", response_model=GetOrderSchema)
def updateOrderById(request: Request,
                    order_id: UUID,
                    payload: CreateOrderSchema):
    with UnitOfWork() as unit_of_work:
        repo = request.app.register_repo(unit_of_work.session)
        order_service = request.app.register_serv(repo)
        order = order_service.search_order(str(order_id))
        if order is None:
            raise HTTPException(
                status_code=404,
                detail=f"Order with ID {order_id} not found"
            )
        order = order_service.update_order(order, payload)
        return order.dict()


@server.delete(
    "/orders/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response)
def deleteOrder(request: Request, order_id: UUID):
    with UnitOfWork() as unit_of_work:
        repo = request.app.register_repo(unit_of_work.session)
        order_service = request.app.register_serv(repo)
        order = order_service.search_order(str(order_id))
        if order is None:
            raise HTTPException(
                status_code=404,
                detail=f"Order with ID {order_id} not found"
            )
        order_service.delete_order(order)


@server.post("/orders/{order_id}/pay", response_model=GetOrderSchema)
def payOrder(request: Request, order_id: UUID):
    with UnitOfWork() as unit_of_work:
        repo = request.app.register_repo(unit_of_work.session)
        order_service = request.app.register_serv(repo)
        order = order_service.search_order(str(order_id))
        if order is None:
            raise HTTPException(
                status_code=404,
                detail=f"Order with ID {order_id} not found"
            )
        order = order_service.update_order_status(order, status="paid")
        order = order_service.schedule_order(order)
        return order.dict()


@server.post("/orders/{order_id}/cancel", response_model=GetOrderSchema)
def cancelOrder(request: Request, order_id: UUID):
    with UnitOfWork() as unit_of_work:
        repo = request.app.register_repo(unit_of_work.session)
        order_service = request.app.register_serv(repo)
        order = order_service.search_order(str(order_id))
        if order is None:
            raise HTTPException(
                status_code=404,
                detail=f"Order with ID {order_id} not found"
            )
        order = order_service.update_order_status(order, status="cancelled")
        order.schedule_order()  # 像这种没有返回对象的方法很适合定义在business层的obj里
        return order.dict()
