from typing import Optional

from trainings_app.repositories.base import BaseRepository
from trainings_app.schemas.clients import CreateClient, GetClient
from trainings_app.exceptions.exceptions import ConvertRecordError, AttrError, CreateRecordError
from trainings_app.logging.repositories import repo_logger
from trainings_app.db.fields.clients import ClientFields


class ClientRepository(BaseRepository):
    fields = ClientFields

    @staticmethod
    def get_client_from_record(record: dict) -> GetClient:
        """Retrieve GetClient model from dict data"""

        if not record:
            repo_logger.error(f"No record found to convert Error")
            raise ConvertRecordError(record=record, error_detail="No record found to convert")
        try:
            return GetClient(**record)
        except AttrError as e:
            repo_logger.error(f"Convert to model Error: {str(e)}")
            raise ConvertRecordError(record=record, error_detail="Invalid data for conversion")

    async def create(self, client: CreateClient) -> GetClient:
        keys, values, indexes = self.data_from_dict(client)
        values_clause = ', '.join([f'${i}' for i in indexes])
        query = f"""
                INSERT INTO clients ({', '.join(keys)})
                VALUES ({values_clause})
                RETURNING {self.fields.get_fields_str()};
            """
        try:
            client_record = await self.db.fetchrow(query, *values)
        except CreateRecordError as e:
            repo_logger.error(f"Creation Error: {str(e)}")
            raise CreateRecordError()
        return self.get_client_from_record(client_record)

    async def get(self, client_id: int) -> GetClient:
        query = f"""
            SELECT {self.fields.get_fields_str()} 
            FROM clients 
            WHERE id = $1;
        """
        client_record = await self.fetchrow_or_404(query, client_id)
        return self.get_client_from_record(client_record)

    async def get_clients(self, filter_params: Optional[dict] = None) -> list[GetClient]:
        query = f"""
            SELECT {self.fields.get_fields_str()}
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
        if not clients_data:
            return []
        return [GetClient(**client) for client in clients_data]

    async def delete(self, client_id: int) -> GetClient:
        query = f"""
            DELETE FROM clients
            WHERE id = $1
            RETURNING {self.fields.get_fields_str()};
        """
        deleted_client = await self.fetchrow_or_404(query, client_id)
        return self.get_client_from_record(deleted_client)

    async def update(self, client_id: int, update_data: dict) -> GetClient:
        keys, values, indexes = self.data_from_dict(update_data)
        if not values:
            repo_logger.error(f"Invalid update data")
            raise AttrError("Invalid update data")
        values.append(client_id)
        set_clause = self.make_set_clause(keys=keys, indexes=indexes)
        query = f"""
            UPDATE {', '.join([key for key in keys])}
            SET {set_clause}
            WHERE id = $1
            RETURNING {self.fields.get_fields_str()};
        """
        updated_client = await self.fetchrow_or_404(query, *values)
        return self.get_client_from_record(updated_client)
