from repository.models import Schedule as ScheduleModel
from service.schedule import Schedule


class ScheduleRepo:
    def __init__(self, sess):
        self.session = sess

    def add(self, schedule_id, name):
        schedule = ScheduleModel(
            id=str(schedule_id), name=name)
        self.session.add(schedule)
        scheduler = Schedule(schedule)
        return scheduler
