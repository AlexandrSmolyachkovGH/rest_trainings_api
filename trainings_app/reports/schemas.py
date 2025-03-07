import json
from datetime import date

from pydantic import BaseModel


class CreateReport(BaseModel):
    report_date_start: date
    report_date_end: date
    new_users: dict


class GetReport(BaseModel):
    id: int
    report_date_start: date
    report_date_end: date
    new_users: dict
