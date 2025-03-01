from typing import Optional

from pydantic import ValidationError

from trainings_app.repositories.base import BaseRepository
from trainings_app.schemas.clients import GetClient
from trainings_app.exceptions.exceptions import ConvertRecordError, AccessError
from trainings_app.custom_loggers.repositories import repo_logger
from trainings_app.db.fields.clients import ClientFields
from trainings_app.schemas.users import GetUser, RoleEnum


class ClientRepository(BaseRepository):
    fields = ClientFields

    @staticmethod
    def __get_client_from_record(record: dict) -> GetClient:
        """Retrieve GetClient model from dict data"""

        if not record:
            repo_logger.error(f"No record found to convert Error")
            raise ConvertRecordError(record=record, error_detail="No record found to convert")
        try:
            return GetClient(**record)
        except ValidationError as e:
            repo_logger.error(f"Convert to model Error: {str(e)}")
            raise ConvertRecordError(record=record, error_detail=f"{str(e)}")

    async def __check_client_access(self, client_id: int, user: GetUser) -> None:
        client = await self.get(client_id)
        if client.user_id != user.id and user.role == RoleEnum.USER:
            raise AccessError

    async def create(self, client: dict) -> GetClient:
        keys, values, indexes = self.data_from_dict(client)
        values_clause = ', '.join([f'${i}' for i in indexes])
        query = f"""
                INSERT INTO clients ({', '.join(keys)})
                VALUES ({values_clause})
                RETURNING {self.fields.get_fields_str()};
            """
        client_record = await self.fetchrow_or_404(query, *values)
        return self.__get_client_from_record(client_record)

    async def get(self, client_id: int) -> GetClient:
        query = f"""
            SELECT {self.fields.get_fields_str()} 
            FROM clients 
            WHERE id = $1;
        """
        client_record = await self.fetchrow_or_404(query, client_id)
        return self.__get_client_from_record(client_record)

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
        clients_data = await self.conn.fetch(query, *values)
        return [GetClient(**client) for client in clients_data]

    async def delete(self, client_id: int, user: GetUser) -> GetClient:
        await self.__check_client_access(client_id=client_id, user=user)
        query = f"""
            DELETE FROM clients
            WHERE id = $1
            RETURNING {self.fields.get_fields_str()};
        """
        deleted_client = await self.fetchrow_or_404(query, client_id)
        return self.__get_client_from_record(deleted_client)

    async def update(self, client_id: int, update_data: dict, user: GetUser) -> GetClient:
        await self.__check_client_access(client_id=client_id, user=user)
        keys, values, indexes = self.data_from_dict(update_data)
        if not values:
            repo_logger.error(f"Invalid update data")
            raise ValidationError("Invalid update data")
        values.append(client_id)
        set_clause = self.make_set_clause(keys=keys, indexes=indexes)
        query = f"""
            UPDATE clients
            SET {set_clause}
            WHERE id = ${len(values)}
            RETURNING {self.fields.get_fields_str()};
        """
        updated_client = await self.fetchrow_or_404(query, *values)
        return self.__get_client_from_record(updated_client)
