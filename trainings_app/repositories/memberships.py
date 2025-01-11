from typing import Optional

from trainings_app.schemas.memberships import CreateMembership, GetMembership, AccessLevelEnum
from trainings_app.repositories.base import BaseRepository
from trainings_app.exceptions.memberships import MembershipsNotFoundError, MembershipsAttrError, \
    ConvertMembershipsRecordError


class MembershipRepository(BaseRepository):
    columns = ['id', 'access_level', 'description', 'price']
    str_columns = ', '.join(columns)

    @staticmethod
    def get_membership_from_record(record: dict) -> GetMembership:
        """Retrieve GetMembership model from dict data"""

        if not record:
            raise ConvertMembershipsRecordError("No record found to convert to GetUser")
        return GetMembership(**record)

    async def create(self, arg: CreateMembership) -> GetMembership:
        keys, values, indexes = self.data_from_dict(arg)
        query = f"""
            INSERT INTO memberships ({', '.join(keys)})
            VALUES ({', '.join([f'${i}' for i in indexes])})
            RETURNING {self.str_columns};
        """
        record = await self.db.fetchrow(query, *values)
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
            raise MembershipsNotFoundError('No relevant entries in the table')

        memberships = [GetMembership(**record) for record in records]
        return memberships

    async def get(self, membership_id: int) -> GetMembership:
        query = f"""
            SELECT {self.str_columns}
            FROM memberships
            WHERE id = $1;
        """
        record = await self.db.fetchrow(query, membership_id)
        if not record:
            raise MembershipsNotFoundError(f"Membership was not found")
        return self.get_membership_from_record(record)

    async def update(self, membership_id: int, changes: dict) -> GetMembership:
        keys, values, indexes = self.data_from_dict(changes)
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
        record = await self.db.fetchrow(query, membership_id)
        if not record:
            raise MembershipsNotFoundError(f"Membership was not found")
        return self.get_membership_from_record(record)
