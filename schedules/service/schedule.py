class Schedule:
    def __init__(self, schedule):
        self.scheduler = schedule

    def dict(self):
        return {
            "id": self.scheduler.id,
            "name": self.scheduler.name,
        }
