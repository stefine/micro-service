class ScheduleService:
    def __init__(self, repo):
        self.repo = repo

    def place_schedule(self, order_id, name):
        schedule = self.repo.add(str(order_id), name)
        return schedule
