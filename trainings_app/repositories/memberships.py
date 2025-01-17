from typing import Optional
from fastapi import HTTPException, status

from trainings_app.db.fields.memberships import MembershipFields
from trainings_app.schemas.memberships import CreateMembership, GetMembership, AccessLevelEnum
from trainings_app.repositories.base import BaseRepository
from trainings_app.exceptions.exceptions import ConvertRecordError, RecordNotFoundError, AttrError
from trainings_app.logging.repositories import repo_logger


class MembershipRepository(BaseRepository):
    columns = MembershipFields.get_fields_list()
    str_columns = MembershipFields.get_fields_str()

    @staticmethod
    def get_membership_from_record(record: dict) -> GetMembership:
        """Retrieve GetMembership model from dict data"""

        if not record:
            repo_logger.error(f"No record found to convert Error")
            raise ConvertRecordError("No record found to convert to GetMembership")
        try:
            return GetMembership(**record)
        except Exception as e:
            repo_logger.error(f"Convert to model Error: {e}")
            raise ConvertRecordError(record=record, model_name="GetMembership",
                                     error_detail="Invalid data for conversion")

    async def create(self, arg: CreateMembership) -> GetMembership:
        keys, values, indexes = self.data_from_dict(arg)
        query = f"""
            INSERT INTO memberships ({', '.join(keys)})
            VALUES ({', '.join([f'${i}' for i in indexes])})
            RETURNING {self.str_columns};
        """
        try:
            record = await self.db.fetchrow(query, *values)
        except Exception as e:
            repo_logger.error(f"Creation Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Membership creation failed. Please try again later."
            )
        return self.get_membership_from_record(record)

    async def get_memberships(self, access_level: Optional[str] = None) -> list[GetMembership]:
        query = f"""
            SELECT {', '.join(c for c in self.columns)}
            FROM memberships
        """
        params = []
        if access_level:
            query += " WHERE access_level = $1"
            params.append(access_level)
        query += ";"
        records = await self.db.fetch(query, *params)
        if not records:
            repo_logger.error(f"No relevant records Error")
            raise RecordNotFoundError(f"No relevant records")
        return [GetMembership(**record) for record in records]

    async def get(self, membership_id: int) -> GetMembership:
        query = f"""
            SELECT {self.str_columns}
            FROM memberships
            WHERE id = $1;
        """
        record = await self.fetchrow_or_404(query, membership_id)
        return self.get_membership_from_record(record)

    async def update(self, membership_id: int, changes: dict) -> GetMembership:
        keys, values, indexes = self.data_from_dict(changes)
        if not values:
            repo_logger.error(f"Invalid update data")
            raise AttrError("Invalid update data")
        values.append(membership_id)
        set_clause = self.make_set_clause(keys=keys, indexes=indexes)
        query = f"""
            UPDATE memberships
            SET {set_clause}
            WHERE id = ${len(indexes) + 1}
            RETURNING {self.str_columns};
        """
        record = await self.fetchrow_or_404(query, *values)
        return self.get_membership_from_record(record)

    async def delete(self, membership_id: int):
        query = f"""
            DELETE FROM memberships
            WHERE id = $1
            RETURNING {self.str_columns};
        """
        record = await self.fetchrow_or_404(query, membership_id)
        return self.get_membership_from_record(record)
