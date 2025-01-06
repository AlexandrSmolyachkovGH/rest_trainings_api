import abc


class BaseRepository(abc.ABC):
    def __init__(self, db):
        self.db = db

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
