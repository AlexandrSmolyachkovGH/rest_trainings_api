import abc


class BaseFields(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_fields_list():
        ...

    @classmethod
    @abc.abstractmethod
    def get_fields_str(cls):
        ...
