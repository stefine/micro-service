from run import server
from starlette import status
from api.schema import GetScheduleSchema, CreateScheduleSchema
from repository.unit_of_work import UnitOfWork
from starlette.requests import Request
from uuid import UUID


@server.post(
    "/schedule/{order_id}/order",
    status_code=status.HTTP_201_CREATED,
    response_model=GetScheduleSchema)
def orderShedule(request: Request,
                 order_id: UUID,
                 payload: CreateScheduleSchema):
    with UnitOfWork() as unit_of_work:
        repo = request.app.register_repo(unit_of_work.session)
        schedule_service = request.app.register_serv(repo)
        name = payload.dict()["name"]
        schedule = schedule_service.place_schedule(order_id, name)
        unit_of_work.commit()
        return schedule.dict()
