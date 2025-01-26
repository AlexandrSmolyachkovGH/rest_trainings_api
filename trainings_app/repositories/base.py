import abc
from asyncpg import Connection

from trainings_app.logging.repositories import repo_logger
from trainings_app.exceptions.exceptions import AttrError, RecordNotFoundError



class BaseRepository(abc.ABC):

    def __init__(self, conn: Connection):
        self.conn = conn

    async def fetchrow_or_404(self, query: str, *args) -> dict:
        """Check for data retrieval. If no data is found, raise a 404 error."""

        record = await self.conn.fetchrow(query, *args)
        if not record:
            repo_logger.error(f"The fetchrow_or_404 Error. No record found for the query.")
            raise RecordNotFoundError()
        return record

    @staticmethod
    def data_from_dict(dct: dict) -> tuple:
        """Returns lists of params for processing"""

        if not isinstance(dct, dict):
            repo_logger.error(f"The data_from_dict Error. Invalid type of passed argument. The required type is Dict.")
            raise AttrError(f"Invalid type of passed argument. The required type is Dict.")

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
