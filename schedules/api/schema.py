from pydantic import BaseModel


class CreateScheduleSchema(BaseModel):
    name: str


class GetScheduleSchema(BaseModel):
    id: str
    name: str
