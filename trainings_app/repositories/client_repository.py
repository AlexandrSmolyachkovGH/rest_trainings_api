from trainings_app.repositories.base import BaseRepository
from typing import Union
from fastapi import HTTPException, status
from trainings_app.schemas.clients import CreateClient, GetClient, GenderEnum


class ConvertClientRecordError(ValueError):
    pass


class ClientAttrError(ValueError):
    pass


class ClientRepository(BaseRepository):
    @staticmethod
    def get_client_from_record(record: dict) -> GetClient:
        """Retrieve GetClient model from dict data"""

        if not record:
            raise ConvertClientRecordError("No record found to convert to GetClient")
        return GetClient(**record)

    @staticmethod
    def client_data_from_client(client: dict) -> tuple:
        """Returns tuple of client params for processing"""

        keys = []
        values = []
        indexes = []
        counter = 0
        for k, v in client.items():
            keys.append(k)
            values.append(v)
            counter += 1
            indexes.append(counter)
        return keys, values, indexes

    async def fetchrow_or_404(self, query: str, *args) -> dict:
        """Check for data retrieval. If no data is found, raise a 404 error."""
        record = await self.db.fetchrow(query, *args)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found."
            )
        return record

    async def create(self, client: CreateClient) -> GetClient:
        keys, values, indexes = self.client_data_from_client(client)
        query = f"""
                INSERT INTO users ({', '.join(keys)})
                VALUES ({', '.join([f'${i}' for i in indexes])})
                RETURNING *;
            """
        client_record = await self.db.fetchrow(query, *values)
        return self.get_client_from_record(client_record)

    async def get(self, client_id: int) -> GetClient:
        query = f"""SELECT * FROM users WHERE id = $1 AND deleted_at IS NULL;"""
        client_record = await self.fetchrow_or_404(query, client_id)
        return self.get_client_from_record(client_record)
