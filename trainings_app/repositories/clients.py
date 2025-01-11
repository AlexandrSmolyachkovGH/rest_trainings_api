from typing import Optional

from trainings_app.repositories.base import BaseRepository
from fastapi import HTTPException, status
from trainings_app.schemas.clients import CreateClient, GetClient, ClientFilters


class ConvertClientRecordError(ValueError):
    pass


class ClientAttrError(ValueError):
    pass


class ClientRepository(BaseRepository):
    fields = ['id', 'user_id', 'membership_id', 'first_name', 'last_name', 'phone_number', 'gender', 'date_of_birth',
              'weight_kg', 'height_cm', 'status']
    fields_str = ', '.join(elem for elem in fields)

    @staticmethod
    def get_client_from_record(record: dict) -> GetClient:
        """Retrieve GetClient model from dict data"""

        if not record:
            raise ConvertClientRecordError("No record found to convert to GetClient")
        return GetClient(**record)

    async def create(self, client: CreateClient) -> GetClient:
        keys, values, indexes = self.data_from_dict(client)
        values_clause = ', '.join([f'${i}' for i in indexes])
        query = f"""
                INSERT INTO clients ({', '.join(keys)})
                VALUES ({values_clause})
                RETURNING {self.fields_str};
            """
        client_record = await self.fetchrow_or_404(query, *values)
        return self.get_client_from_record(client_record)

    async def get(self, client_id: int) -> GetClient:
        query = f"""
            SELECT {self.fields_str} 
            FROM clients 
            WHERE id = $1;
        """
        client_record = await self.fetchrow_or_404(query, client_id)
        return self.get_client_from_record(client_record)

    async def get_clients(self, filter_params: Optional[dict] = None) -> list[GetClient]:
        query = f"""
            SELECT {self.fields_str}
            FROM clients
        """
        values = []
        if filter_params:
            keys, values, indexes = self.data_from_dict(filter_params)
            where_clause = ' AND '.join([f"{k} = ${i}" for k, i in zip(keys, indexes)])
            query += f"""
                WHERE {where_clause}
            """
        query += ';'
        clients_data = await self.db.fetch(query, *values)
        clients_list = [GetClient(**client) for client in clients_data]
        return clients_list

    async def delete(self, client_id: int) -> GetClient:
        query = f"""
            DELETE FROM clients
            WHERE id = $1
            RETURNING {self.fields_str};
        """
        deleted_client = await self.fetchrow_or_404(query, client_id)
        return self.get_client_from_record(deleted_client)

    async def update(self, client_id: int, update_data: dict) -> GetClient:
        keys, values, indexes = self.data_from_dict(update_data)
        values.append(client_id)
        set_clause = self.make_set_clause(keys=keys, indexes=indexes)
        query = f"""
            UPDATE {', '.join([key for key in keys])}
            SET {set_clause}
            WHERE id = $1
            RETURNING {self.fields_str};
        """
        updated_client = self.fetchrow_or_404(query, *values)
        return self.get_client_from_record(updated_client)
