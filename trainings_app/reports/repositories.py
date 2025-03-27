import json

from trainings_app.db.fields.report import ReportFields
from trainings_app.reports.schemas import GetReport
from trainings_app.repositories.base import BaseRepository


class ReportRepository(BaseRepository):
    fields = ReportFields

    async def create(self, dct: dict) -> GetReport:
        dct["new_users"] = json.dumps(dct["new_users"])
        keys, values, indexes = self.data_from_dict(dct)
        query = f"""
            INSERT INTO simple_report ({', '.join(keys)})
            VALUES ({', '.join([f'${i}' for i in indexes])})
            RETURNING {self.fields.get_fields_str()};
        """
        record = await self.conn.fetchrow(query, *values)
        record_dict = dict(record)
        if isinstance(record_dict["new_users"], str):
            record_dict["new_users"] = json.loads(record_dict["new_users"])
        return GetReport(**record_dict)

    async def get(self, *args, **kwargs):
        ...

    async def delete(self, *args, **kwargs):
        ...

    async def update(self, *args, **kwargs):
        ...
