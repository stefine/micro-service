from server import create_server
from repository.schedule_repository import ScheduleRepo
from service.schedule_service import ScheduleService

server = create_server(ScheduleRepo, ScheduleService)

from api import api
