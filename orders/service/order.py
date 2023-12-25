import requests
from service.exceptions import APIIntegrationError


class Order:
    def __init__(self, record):
        self.record = record

    @property
    def id(self):
        return self.record.id

    def dict(self):
        return {
            "id": self.record.id,
            "created": self.record.created,
            "status": self.record.status,
            "order": self.record.order.dict(),
        }

    def schedule_order(self):
        schedule_base_url = "http://localhost:3000/schedule"
        response = requests.post(
            f"{schedule_base_url}/{str(self.id)}/order",
            json={"name": "schdule1"},
        )
        if response.status_code == 201:
            return
        else:
            raise APIIntegrationError(
                f'Could not cancel order with id {self.id}')
