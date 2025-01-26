from typing import Optional
from pydantic import ValidationError

from trainings_app.db.fields.memberships import MembershipFields
from trainings_app.schemas.memberships import CreateMembership, GetMembership
from trainings_app.repositories.base import BaseRepository
from trainings_app.exceptions.exceptions import ConvertRecordError
from trainings_app.logging.repositories import repo_logger


class MembershipRepository(BaseRepository):
    fields = MembershipFields

    @staticmethod
    def __get_membership_from_record(record: dict) -> GetMembership:
        """Retrieve GetMembership model from dict data"""

        if not record:
            repo_logger.error(f"No record found to convert Error")
            raise ConvertRecordError(record=record, error_detail="No record found to convert")
        try:
            return GetMembership(**record)
        except ValidationError as e:
            repo_logger.error(f"Convert to model Error: {str(e)}")
            raise ConvertRecordError(record=record, error_detail=f"{str(e)}")

    async def create(self, arg: CreateMembership) -> GetMembership:
        keys, values, indexes = self.data_from_dict(arg)
        query = f"""
            INSERT INTO memberships ({', '.join(keys)})
            VALUES ({', '.join([f'${i}' for i in indexes])})
            RETURNING {self.fields.get_fields_str()};
        """
        record = await self.fetchrow_or_404(query, *values)
        return self.__get_membership_from_record(record)

    async def get_memberships(self, access_level: Optional[str] = None) -> list[GetMembership]:
        query = f"""
            SELECT {self.fields.get_fields_str()}
            FROM memberships
        """
        params = []
        if access_level:
            query += " WHERE access_level = $1"
            params.append(access_level)
        query += ";"
        records = await self.conn.fetch(query, *params)
        return [GetMembership(**record) for record in records]

    async def get(self, membership_id: int) -> GetMembership:
        query = f"""
            SELECT {self.fields.get_fields_str()}
            FROM memberships
            WHERE id = $1;
        """
        record = await self.fetchrow_or_404(query, membership_id)
        return self.__get_membership_from_record(record)

    async def update(self, membership_id: int, update_data: dict) -> GetMembership:
        keys, values, indexes = self.data_from_dict(update_data)
        if not values:
            repo_logger.error(f"Invalid update data")
            raise ValidationError("Invalid update data")
        values.append(membership_id)
        set_clause = self.make_set_clause(keys=keys, indexes=indexes)
        query = f"""
            UPDATE memberships
            SET {set_clause}
            WHERE id = ${len(indexes) + 1}
            RETURNING {self.fields.get_fields_str()};
        """
        record = await self.fetchrow_or_404(query, *values)
        return self.__get_membership_from_record(record)

    async def delete(self, membership_id: int):
        query = f"""
            DELETE FROM memberships
            WHERE id = $1
            RETURNING {self.fields.get_fields_str()};
        """
        record = await self.fetchrow_or_404(query, membership_id)
        return self.__get_membership_from_record(record)
