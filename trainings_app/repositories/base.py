import abc
from fastapi import HTTPException, status


class BaseFields(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_fields_list():
        ...

    @staticmethod
    @abc.abstractmethod
    def get_fields_str():
        ...


class BaseRepository(abc.ABC):
    def __init__(self, db):
        self.db = db

    async def fetchrow_or_404(self, query: str, *args) -> dict:
        """Check for data retrieval. If no data is found, raise a 404 error."""
        record = await self.db.fetchrow(query, *args)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found."
            )
        return record

    @staticmethod
    def data_from_dict(dct: dict) -> tuple:
        """Returns lists of params for processing"""

        keys = []
        values = []
        indexes = []
        counter = 0
        for k, v in dct.items():
            keys.append(k)
            values.append(v)
            counter += 1
            indexes.append(counter)
        return keys, values, indexes

    @staticmethod
    def make_set_clause(keys: list, indexes: list) -> str:
        """Construct the lists of keys and indexes into a string for the SET clause."""
        set_clause = ", ".join([f"{key} = ${idx}" for key, idx in zip(keys, indexes)])
        return set_clause

    @abc.abstractmethod
    async def get(self, *args, **kwargs):
        """An abstract method for describing the behavior of get requests"""
        ...

    @abc.abstractmethod
    async def create(self, *args, **kwargs):
        """An abstract method for describing the behavior of post requests"""
        ...

    @abc.abstractmethod
    async def delete(self, *args, **kwargs):
        """An abstract method for describing the behavior of delete requests"""
        ...

    @abc.abstractmethod
    async def update(self, *args, **kwargs):
        """An abstract method for describing the behavior of put and patch requests"""
        ...
